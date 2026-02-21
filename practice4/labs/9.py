n= int(input())
def sq(a):
    num = 0
    while (num<=a):
        yield 2**num
        num+=1
for i in sq(n): print(i,end=" ")