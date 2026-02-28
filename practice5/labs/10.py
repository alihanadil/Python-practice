import re
n = input()
s = re.search("dog|cat", n)
if s: print("Yes")
else: print("No")