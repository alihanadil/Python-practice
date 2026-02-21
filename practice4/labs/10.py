n = input().split()
k = int(input())
def l(n,k):
    cnt = 1
    while (cnt<=k):
        for i in n: yield i
        cnt+=1
for i in l(n,k): print(i,end=" ")