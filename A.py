n = int(input())
dors = {}
for i in range(n):
    els = input().split()
    key = els[0]
    value = int(els[1])
    if key in dors: dors[key] += value
    else: dors[key] = value
dors = dict(sorted(dors.items()))
for i, j in dors.items():
    print(i, j)

