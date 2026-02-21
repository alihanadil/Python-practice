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
