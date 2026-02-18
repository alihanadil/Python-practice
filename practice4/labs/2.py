n = int(input())
def square(a):
    even = 0
    while (even<=a): 
        yield even
        even +=2
print(*square(n), sep =",")