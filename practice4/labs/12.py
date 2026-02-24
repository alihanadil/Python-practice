import json
def serialize(val):
    if val is None:
        return 'null'
    return json.dumps(val, separators=(',', ':'))
def compare(a, b , path, results):
    if isinstance(a, dict) and isinstance(b, dict):
        allKeys = set(a.keys() | b.keys())
        for key in sorted(allKeys):
            newPath = f"{path}.{key}" if path else key
            if key not in a: results.append((newPath, "<missing>", serialize(b[key])))
            elif key not in b: results.append((newPath, serialize(a[key]), "<missing>"))
            else: compare(a[key], b[key], newPath, results)
    else:
        if a!=b: results.append((path, serialize(a), serialize(b)))

diff = []
obj1 = json.loads(input().strip())
obj2 = json.loads(input().strip())
compare(obj1, obj2, "", diff)
if not diff: print("No differences")
else:
    diff.sort(key=lambda x: x[0])
    for path, old, new in diff: print(f"{path} : {old} -> {new}")