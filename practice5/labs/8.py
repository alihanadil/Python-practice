import re
n = input()
m = input()
result = re.split(m, n)

for i in range(len(result)):
    if i != 0: print(",", end="")
    print(result[i],end="")