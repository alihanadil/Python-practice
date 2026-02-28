import re
n = input()
s = re.findall(r"[A-Z]", n)
print(len(s))