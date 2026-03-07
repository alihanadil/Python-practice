n = int(input())
lst1 = list(map(int, input().split()))
cnt = sum(map(bool, lst1))

# lst1 = list(filter(lambda x:bool(x) ,list(map(int, input().split()))))
# print(len(lst1))
print(cnt)

