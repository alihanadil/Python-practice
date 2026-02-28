import re
n = input()
if re.findall("\d$",n) and re.findall("^[a-zA-Z]", n):  print("Yes")
else: print("No")