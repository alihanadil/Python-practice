import re
n = input()
result = re.match("Hello", n)
if result: print("Yes")
else: print("No")