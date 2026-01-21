#both types of quotes are strings

print("Hello")
print('Hello')

b = "Hello,"
print(b[2:5]) #slicing of a string, "llo" will be printed out
print(b[::-1]) # -1 at the end means the string will be written from the end
print(b.upper())
print(b.lower())
a = "World!" 
print(b+a) #concatenation of strings
age = 36
txt = f"My name is John, I am {age}" #To specify a string as an f-string, simply put an f in front of the string literal, and add curly brackets {} as placeholders for variables and other operations.
print(txt)