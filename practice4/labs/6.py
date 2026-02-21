n = int(input())
def fib(a):
    cnt = 0
    n1 = 0
    n2 = 1
    if (a==0):
        return
    elif (a==1):
        yield 0
    else:

        while(cnt+1<a):
            yield n1+n2
            n1 = n1 + n2
            n2 = n1 - n2
            cnt +=1
            
if(n == 1): print(0)
if (n>1):
    print(0, end="")
    for i in fib(n):
        print(",", i,end="", sep="")