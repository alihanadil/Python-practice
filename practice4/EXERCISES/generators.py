#1 Create a generator that generates the squares of numbers up to some number N.
# n = int(input())
# def square(n):
#     count = 1
#     while (count<=n): 
#         yield count
#         count +=1
# for num in square(n): print(num**2)

#2 Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.
n = int(input())
def square(a):
    even = 2
    while (even<=a): 
        yield even
        even +=2
if (n == 0): print(0)
else:
    print(0,end="")
    for i in square(n):
        print(",", i, sep="", end="")

#3 Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.
n = int(input())
def div(a):
    start = 0
    while(start<=a):
        yield start
        start +=12
for i in div(n): print(i,end=" ")
#4 Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.
n, m = list(map(int,input().split()))
def sq(a,b):
    while(a<= b):
        yield a**2
        a +=1
for i in sq(n,m): print(i)
#5 Implement a generator that returns all numbers from (n) down to 0.
n = int(input())
def cnt(a):
    cnt = a
    while(cnt>=0):
        yield cnt
        cnt-=1
for i in cnt(n):print(i)
