import json
source = json.loads(input().strip())
n = int(input())
keys = []
for j in range(n):
    k = []
    a = input()
    i = 0
    item = ""
    while i < len(a):
        if a[i] == "." or a[i] == "[":
            if a[i] == "[":
                if item:
                    k.append(("key", item))
                    item = ""
                i += 1
                ind = ""
                while a[i] != "]":
                    ind += a[i]
                    i += 1
                i += 1
                k.append(("index", int(ind)))
            else: 
                if item:
                    k.append(("key", item))
                    item = ""
                i += 1
        else:
            item += a[i]
            i += 1
    if item:
        k.append(("key", item))
    keys.append(k)

for s in keys:
    cur = source
    found = True
    for typ, val in s:
        if typ == 'key':
            if isinstance(cur, dict) and val in cur:
                cur = cur[val]
            else: 
                found = False
                break
        else:
            if isinstance(cur, list) and 0 <= val < len(cur):
                cur = cur[val]
            else:
                found = False
                break
    if found:
            print(json.dumps(cur, separators=(',', ':')))
    else:
        print("NOT_FOUND")
            

