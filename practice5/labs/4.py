import re
n = input()
res = re.findall("\d", n)
for i in res: print(i, end=" ")