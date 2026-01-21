# 1. both types of quotes are strings

print("Hello")
print('Hello')

#2. Slicing and Indexing
b = "Hello,"
print(b[2:5]) #slicing of a string, "llo" will be printed out
print(b[::-1]) # -1 at the end means the string will be written from the end

#3. Examples of string functions
print(b.upper())
print(b.lower())

#4. concatenation of strings
a = "World!" 
print(b+a) 

#5 Example of an f-string
age = 36
txt = f"My name is John, I am {age}"
print(txt)