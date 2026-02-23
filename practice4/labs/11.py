import json

def apply_patch(src, patch):
    for k, v in patch.items():
        if v is None:
            src.pop(k, None)
        elif k in src and isinstance(src[k], dict) and isinstance(v, dict):
            src[k] = apply_patch(src[k], v)
        else:
            src[k] = v
    return src

source = json.loads(input().strip())
patch = json.loads(input().strip())
result = apply_patch(source, patch)
print(json.dumps(result, sort_keys=True, separators=(',', ':')))