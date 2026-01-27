#1
x = 5
y = "Hello, World!"
X = 6 # X and x are different variables therefore x's value will be unchanged

#2 legal variable names
myvar = "John"
my_var = "John"
_my_var = "John"
myVar = "John"
MYVAR = "John"
myvar2 = "John"

#2.5 illegal variable names
2myvar = "John"
my-var = "John"
my var = "John"

#3 Python allows you to assign values to multiple variables in one line:
q, w, e = "Orange", "Banana", "Cherry"
print(q)
print(w)
print(e)

# or unpacking a list
fruits = ["apple", "banana", "cherry"]
q, w, e = fruits
print(q)
print(w)
print(e)

#4 Global and local variables
x = "awesome" #global, can be used anywhere in the code

def myfunc():
  x = "fantastic" #local, can't be used outside of a function
  print("Python is " + x)

myfunc()