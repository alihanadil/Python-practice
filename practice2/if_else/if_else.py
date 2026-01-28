#The else keyword catches anything which isn't caught by the preceding conditions.
#The else statement is executed when the if condition (and any elif conditions) evaluate to False.
a = 200
b = 33
if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

#------
number = 7

if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")