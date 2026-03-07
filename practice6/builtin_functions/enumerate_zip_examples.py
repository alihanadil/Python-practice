"""
enumerate_zip_examples.py - concise examples of enumerate() and zip().
"""

# ===== enumerate() =====
print("enumerate():")
fruits = ['apple', 'banana', 'cherry']
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# start parameter
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}: {fruit}")
# find indices of a value
nums = [10, 20, 30, 20]
indices = [i for i, v in enumerate(nums) if v == 20]
print("Indices of 20:", indices)

# ===== zip() =====
print("\nzip():")
names = ['Alice', 'Bob', 'Charlie']
scores = [85, 92, 78]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
# zipped list
pairs = list(zip(names, scores))
print(pairs)
# unequal lengths - truncation
short = [1, 2]
long = ['a', 'b', 'c']
print("zip truncates:", list(zip(short, long)))
# build dict
keys = ['name', 'age']
vals = ['Alice', 30]
d = dict(zip(keys, vals))
print("dict from zip:", d)

# ===== combine enumerate and zip =====
print("\ncombined:")
items = ['pen', 'pencil']
prices = [1.5, 0.8]
for i, (item, price) in enumerate(zip(items, prices), 1):
    print(f"{i}. {item} ${price}")