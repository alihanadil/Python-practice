import re
n = input()
pattern = r'\S+@\S+\.\S+'
s = re.search(pattern, n)
if s: print(s.group())
else: print("No email")