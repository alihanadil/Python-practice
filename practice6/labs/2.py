def is_even(x):
    return x %2 == 0
n = int(input())
lst = list(filter(is_even, list(map(int, input().split()))))
print(len(lst))