#If you do not know how many arguments will be passed into your function, add a * before the parameter name.
#This way, the function will receive a tuple of arguments and can access the items accordingly:
def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus") 

#The *args parameter allows a function to accept any number of positional arguments.
def my_function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function("Emil", "Tobias", "Linus") 

#You can combine regular parameters with *args.
#Regular parameters must come before *args:
def my_function(greeting, *names):
  for name in names:
    print(greeting, name)

my_function("Hello", "Emil", "Tobias", "Linus") 