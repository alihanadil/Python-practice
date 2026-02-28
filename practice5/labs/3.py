import re
n = input()
m = input()
res = re.findall(m, n)
print(len(res))