n = int(input())
def primes(a):
    cnt = 2
    while(cnt<=a):
        isPrime = True
        for i in range(2, int(cnt**0.5) + 1):
            if cnt % i == 0:
                isPrime = False
                break
        if isPrime: yield cnt
        cnt+=1
for i in primes(n): print(i, end = " ")