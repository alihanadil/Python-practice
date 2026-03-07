n = int(input())
lst =  sum(list(map(lambda x: x**2, list(map(int, input().split())))))
print(lst)