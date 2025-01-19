file = open('C:/Users/HP/OneDrive/Documents/Coding/ANNJY/PYTHON/File1.txt','r')
print("Reading first line...")
print(file.readline())
file.close()


file = open('C:/Users/HP/OneDrive/Documents/Coding/ANNJY/PYTHON/File1.txt','r')
print("Reading multiple line...")
print(file.readline())
print(file.readline())
print(file.readline())
print(file.readline())
file.close()

file = open('C:/Users/HP/OneDrive/Documents/Coding/ANNJY/PYTHON/File1.txt','r')
print("looping through the  line...")
for line in file:
    print(line)
file.close() 