n = int(input())
nums = list(map(int, input().split()))
actn = int(input())
actions = []
for i in range(actn):
    # actions.append(input().split())
    a = input().split()
    if (a[0] == "abs"):
        nums = list(map(lambda x: abs(x), nums.copy()))
    if (a[0] == "add"):
        nums = list(map(lambda x: x + int(a[1]), nums.copy()))
    if (a[0] == "multiply"):
        nums = list(map(lambda x: x * int(a[1]), nums.copy()))
    if (a[0] == "power"):
        nums = list(map(lambda x: x ** int(a[1]), nums.copy()))
for i in nums: print(i, end=" ")