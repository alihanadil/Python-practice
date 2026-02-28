import re
n = input().strip()
r = re.findall(r'\b[a-zA-Z]{3}\b', n)
print(len(r))