n = int(input())
def div(a):
    start = 0
    while(start<=a):
        yield start
        start +=12
for i in div(n): print(i,end=" ")