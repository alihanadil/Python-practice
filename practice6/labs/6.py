n = int(input())
lst1 = list(map(int, input().split()))

a = all(i>=0 for i in lst1)
if a: print("Yes")
else: print("No")