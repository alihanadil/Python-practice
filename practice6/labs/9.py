n = int(input())
keys = input().split()
vals = input().split()
dic = dict(zip(keys, vals))
k = input()

if k in dic: print(dic[k])
else: print("Not found")