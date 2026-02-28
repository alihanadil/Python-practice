import re
n = input()
m = input()
change = input()

print(re.sub(m, change, n))