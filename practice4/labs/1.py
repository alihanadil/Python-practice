n = int(input())
def square(n):
    count = 1
    while (count<=n): 
        yield count**2
        count +=1
for num in square(n): print(num)