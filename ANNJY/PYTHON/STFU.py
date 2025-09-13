def primeseive(n):
    prime = [True for i in range(n+1)]
    p = 2
    while (p * p <= n):
        if (prime[p] == True):
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1
    prime[0]=False
    prime[1]=False
    return prime
n=int(input("Enter number to find all primes up to that number: "))
primeseive(n)
print("Following are the prime numbers smaller", n)
print("than or equal to", n)