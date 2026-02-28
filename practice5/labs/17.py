import re
n = input()
patt = r'\d{2}/\d{2}/\d{4}'
s = re.findall(patt, n)
print(len(s))