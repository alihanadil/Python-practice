n = int(input())
def valid(num):
    isEven = True
    while(num > 0):
        if num % 2 !=0:
            isEven = False
            break
        san = num % 10
        if (san % 2 == 0): num //= 10
        else: 
            isEven = False
            break
    if isEven: print("Valid")
    else: print("Not valid")
valid(n)