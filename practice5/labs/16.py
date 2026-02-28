import re
n = input()
patt = r'Name: (\D+), Age: (\d+)'
mat = re.search(patt, n)
if mat: print(mat.group(1), mat.group(2))