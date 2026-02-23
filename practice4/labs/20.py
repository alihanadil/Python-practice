s = int(input())
vars = {}
g = 0
n = 0
for i in range(s):
    a, b = input().split()
    if a == "global": g+=int(b)
    elif a == "nonlocal": n+=int(b)
print(g, n)
