#The elif keyword is Python's way of saying "if the previous conditions were not true, then try this condition".
#The elif keyword allows you to check multiple expressions for 
#True and execute a block of code as soon as one of the conditions evaluates to True.
a = 200
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")

#-----------
age = 25

if age < 13:
  print("You are a child")
elif age < 20:
  print("You are a teenager")
elif age < 65:
  print("You are an adult")
else:
  print("You are a senior")