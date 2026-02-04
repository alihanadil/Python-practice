n = input()
nums = ["ZER","ONE", "TWO", "THR", "FOU", "FIV", "SIX", "SEV", "EIG", "NIN"]
act = ['+', '-', "*", '/']
actual = ""
len1 = 0
for i in n:
    if i not in act:
        len1 +=1
    if i in act:
        actual = i
        break
num1 = n[:len1]
real1 = ""
real2 = ""
num2 = n[len1+1:]
for i in range(0,len(num1),3):
    # print(i)
    for j in range(10):
        if num1[i:i+3] == nums[j]:
            real1 = real1 + str(j)
for i in range(0,len(num2),3):
    for j in range(10):
        if num2[i:i+3] == nums[j]:  
            real2 = real2 + str(j)
ans = ""
if actual == "+": ans += str(int(real1) + int(real2))
elif actual == "-": ans += str(int(real1) - int(real2))
elif actual == "*": ans += str(int(real1) * int(real2))
else: ans += str(int(real1) / int(real2))
realans = ""
for i in range(len(ans)):
    for j in range(10):
        if int(ans[i]) == j:
            realans += nums[j]
print(realans)