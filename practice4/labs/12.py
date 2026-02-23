import json
def dif(o1, o2):
    for i, j in o2.items():
        if i not in o1: print(i, ": <missing>", "->", j)
        elif i in o1 and o1[f"{i}"] != j: print(i, ":", o1[f"{i}"], "->", j)
    if o1 == o2: print("No differences")
        


source = json.loads(input().strip())
patch = json.loads(input().strip())
dif(source, patch)
