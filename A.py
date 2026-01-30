n = int(input())
db = {}
for i in range(n):
    els = input().split(maxsplit=2)
    keys = els[1]
    if els[0] == "set": db[keys] = els[2]
    if els[0] == "get":
        print(db[keys] if keys in db else f"KE: no key {keys} found in the document")