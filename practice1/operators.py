#arithmethic operators
x = 15
y = 4

print(x + y)
print(x * y)    
print(x % y)
print(x ** y)
print(x // y)

# Basic assignment 
x = 10
x += 5 

# Bitwise assignment
y = 12      # Binary: 1100
y &= 5      # y is now 4 (1100 & 0101 = 0100)
y |= 3      # y is now 7 (0100 | 0011 = 0111)
y ^= 1      # y is now 6 (0111 ^ 0001 = 0110)


# comparison operators
x = 5
y = 3

print(x == y)
print(x != y)
print(x > y)
print(x <= y) 

#logical
x = 5
print(x > 0 and x < 10)
x = 5
print(x < 5 or x > 10)
x = 5
print(not(x > 3 and x < 10))

#identity (is, is not)
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x
print(x is z)
print(x is y)

x = ["apple", "banana"]
y = ["apple", "banana"]

print(x is not y)

#membership
fruits = ["apple", "banana", "cherry"]

print("banana" in fruits)