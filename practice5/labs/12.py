import re
n = input()
s = re.findall("[0-9][0-9]+", n)
for i in s: print(i, end=" ")