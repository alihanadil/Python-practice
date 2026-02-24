import importlib
n = int(input())
for i in range(n):
    mod, att = input().split()
    try:
        module = importlib.import_module(mod)
        if hasattr(module, att):
            value = getattr(module, att, "Not found")
            if callable(value): print("CALLABLE") 
            else: print("VALUE")
        else: print("ATTRIBUTE_NOT_FOUND")
    except ImportError:
        print("MODULE_NOT_FOUND")