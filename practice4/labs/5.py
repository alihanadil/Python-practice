n = int(input())
def cnt(a):
    cnt = a
    while(cnt>=0):
        yield cnt
        cnt-=1
for i in cnt(n):print(i)