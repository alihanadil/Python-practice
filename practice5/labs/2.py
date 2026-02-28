import re
n = input()
m = input()
if re.search(m, n):    print("Yes")
else: print("No")