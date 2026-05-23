# file: settings.py

# Game settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Player settings
PLAYER_SPEED = 300  # pixels per second
PLAYER_HEALTH = 100

# Bullet settings
BULLET_SPEED = 500
BULLET_LIFETIME = 2.0  # seconds


SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000
TICK_RATE = 20 



import pygame
import uuid
from pygame.math import Vector2

class Player:
    def _init_(self, x, y, name="Player"):
        self.id = str(uuid.uuid4())  # unique identifier
        self.name = name
        self.pos = Vector2(x, y)
        self.vel = Vector2(0, 0)
        self.health = settings.PLAYER_HEALTH
        self.is_alive = True
        self.last_shot_time = 0
        self.fire_rate = 0.5  # seconds between shots

    def move(self, dx, dy, dt):
        self.vel = Vector2(dx, dy).normalize() * settings.PLAYER_SPEED if dx or dy else Vector2(0,0)
        self.pos += self.vel * dt
        # clamp to screen
        self.pos.x = max(0, min(settings.WIDTH, self.pos.x))
        self.pos.y = max(0, min(settings.HEIGHT, self.pos.y))

    def can_shoot(self, current_time):
        return (current_time - self.last_shot_time) >= self.fire_rate

    def shoot(self, target_pos, current_time):
        if not self.can_shoot(current_time):
            return None
        self.last_shot_time = current_time
        direction = Vector2(target_pos) - self.pos
        direction = direction.normalize()
        return Bullet(self.id, self.pos, direction)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.is_alive = False

# file: bullet.py

import pygame
from pygame.math import Vector2

class Bullet:
    def _init_(self, owner_id, start_pos, direction):
        self.owner_id = owner_id
        self.pos = Vector2(start_pos)
        self.dir = direction
        self.speed = settings.BULLET_SPEED
        self.lifetime = settings.BULLET_LIFETIME
        self.alive_time = 0

    def update(self, dt):
        self.pos += self.dir * self.speed * dt
        self.alive_time += dt
        if self.alive_time >= self.lifetime:
            return False  # indicates bullet should be removed
        # optionally, if collides with wall or outside screen: return False
        return True

# file: server.py

import socket
import threading
import time
import pickle

from settings import SERVER_IP, SERVER_PORT, TICK_RATE
from player import Player
from bullet import Bullet

class GameServer:
    def _init_(self):
        self.players = {}  # player_id -> Player
        self.bullets = []  # list of Bullet
        self.lock = threading.Lock()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((SERVER_IP, SERVER_PORT))
        self.sock.listen()
        print("Server listening on", SERVER_IP, SERVER_PORT)
        self.clients = {}  # player_id -> client socket

    def handle_client(self, client_sock, addr):
        # initial handshake: receive player name
        data = client_sock.recv(1024)
        name = pickle.loads(data)
        player = Player(settings.WIDTH/2, settings.HEIGHT/2, name=name)
        with self.lock:
            self.players[player.id] = player
            self.clients[player.id] = client_sock
        print(f"Player {player.name} connected: {player.id}")
        try:
            while True:
                data = client_sock.recv(4096)
                if not data:
                    break
                msg = pickle.loads(data)
                # msg might be: { 'type': 'input', 'dx':..., 'dy':..., 'shoot':True/False, 'target':(x,y) }
                with self.lock:
                    if msg['type'] == 'input':
                        p = self.players.get(player.id)
                        if not p or not p.is_alive:
                            continue
                        # move
                        p.move(msg['dx'], msg['dy'], msg['dt'])
                        # shoot
                        if msg.get('shoot'):
                            bullet = p.shoot(msg['target'], msg['current_time'])
                            if bullet:
                                self.bullets.append(bullet)
        finally:
            with self.lock:
                if player.id in self.players:
                    del self.players[player.id]
                    del self.clients[player.id]
            client_sock.close()
            print(f"Player {player.id} disconnected")

    def run(self):
        # accept clients
        threading.Thread(target=self.accept_clients, daemon=True).start()
        tick_interval = 1.0 / TICK_RATE
        last = time.time()
        while True:
            now = time.time()
            dt = now - last
            if dt < tick_interval:
                time.sleep(tick_interval - dt)
                continue
            last = now
            self.update_game(dt)
            self.send_state()

    def accept_clients(self):
        while True:
            client, addr = self.sock.accept()
            threading.Thread(target=self.handle_client, args=(client, addr), daemon=True).start()

    def update_game(self, dt):
        with self.lock:
            # update bullets
            new_bullets = []
            for b in self.bullets:
                alive = b.update(dt)
                if not alive:
                    continue
                # check collision with players
                for pid, p in self.players.items():
                    if pid == b.owner_id or not p.is_alive:
                        continue
                    # simple distance check
                    if (p.pos - b.pos).length() < 20:  # radius
                        p.take_damage(20)
                        alive = False
                        break
                if alive:
                    new_bullets.append(b)
            self.bullets = new_bullets

    def send_state(self):
        # prepare a snapshot of current game state
        state = {
            'players': {pid: {'pos': (p.pos.x, p.pos.y), 'health': p.health, 'is_alive': p.is_alive} for pid, p in self.players.items()},
            'bullets': [ (b.owner_id, (b.pos.x, b.pos.y)) for b in self.bullets ]
        }
        data = pickle.dumps(state)
        with self.lock:
            for pid, client in self.clients.items():
                try:
                    client.sendall(data)
                except:
                    # handle broken connections
                    pass

if _name_ == '_main_':
    import settings
    server = GameServer()
    server.run()

# file: client.py

import pygame
import socket
import threading
import time
import pickle

from settings import WIDTH, HEIGHT, FPS, SERVER_IP, SERVER_PORT
from player import Player  # client might use this class for local prediction etc

def receive_thread(sock, game_state):
    while True:
        data = sock.recv(4096)
        if not data:
            continue
        state = pickle.loads(data)
        # update local representation of other players & bullets
        game_state['state'] = state

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))

    name = input("Enter your name: ")
    sock.sendall(pickle.dumps(name))

    game_state = {'state': None}

    threading.Thread(target=receive_thread, args=(sock, game_state), daemon=True).start()

    # local player
    local_player = Player(WIDTH/2, HEIGHT/2, name=name)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_d]:
            dx = 1

        mouse_pos = pygame.mouse.get_pos()
        can_shoot = False
        if pygame.mouse.get_pressed()[0]:
            can_shoot = True

        # send input to server
        msg = {
            'type': 'input',
            'dx': dx,
            'dy': dy,
            'dt': dt,
            'shoot': can_shoot,
            'target': mouse_pos,
            'current_time': time.time()
        }
        sock.sendall(pickle.dumps(msg))

        # Draw
        screen.fill((30, 30, 30))
  
        if game_state['state']:
            for pid, pdata in game_state['state']['players'].items():
                color = (0,255,0) if pid != local_player.id else (0,0,255)
                pygame.draw.circle(screen, color, (int(pdata['pos'][0]), int(pdata['pos'][1])), 15)
            for b in game_state['state']['bullets']:
                _, (bx, by) = b
                pygame.draw.circle(screen, (255,255,0), (int(bx), int(by)), 5)

        # update local player (client‐side prediction optional)
        local_player.move(dx, dy, dt)
        # maybe draw local player
        pygame.draw.circle(screen, (0,0,255), (int(local_player.pos.x), int(local_player.pos.y)), 15)

        pygame.display.flip()

    pygame.quit()
