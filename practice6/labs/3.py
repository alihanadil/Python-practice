n = int(input())
lst = input().split()

for index, item in enumerate(lst, start=0):
    print(f'{index}:{item}', end=" ")