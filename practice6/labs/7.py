n = int(input())
lst = input().split()
res = max(lst, key=len)
print(res)