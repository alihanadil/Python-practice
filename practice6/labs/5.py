n = input()
def hasVow(s):
    for i in s: 
        if i in "aeiouAEIOU": return True
    return False
h = hasVow(n)
if h: print("Yes")
else: print("No")