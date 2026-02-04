#Syntax: lambda arguments : expression
x = lambda a : a + 10
print(x(5)) 

#Lambda functions can take any number of arguments:
x = lambda a, b : a * b
print(x(5, 6)) 

x = lambda a, b, c : a + b + c
print(x(5, 6, 2))

#The power of lambda is better shown when you use them as an anonymous function inside another function.
#Say you have a function definition that takes one argument, and that argument will be multiplied with an unknown number:
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11)) 

