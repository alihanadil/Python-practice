n, m = list(map(int,input().split()))
def sq(a,b):
    while(a<= b):
        yield a
        a +=1
for i in sq(n,m): print(i**2)