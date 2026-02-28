import re
#1 Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.
n = input()
match = re.search(r'ab*', n)
if match: print(match.group())
else: print("No match")

#2 Write a Python program that matches a string that has an 'a' followed by two to three 'b'.
match = re.search(r'ab{2,3}', n)
if match: print(match.group())
else: print("No match")

#3 Write a Python program to find sequences of lowercase letters joined with a underscore.
match = re.findall(r'\b[a-z]+(?:_[a-z]+)*\b', n)
if match:
    for m in match: print(m)  
else: print("No match")
   

#4 Write a Python program to find the sequences of one upper case letter followed by lower case letters.
match = re.findall(r'[A-Z][a-z]+', n)
if match:
    for m in match: print(m)
else: print("No match")
    

#5 Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.
match = re.search(r'a.*b$', n)
if match: print(match.group())
else: print("No match")

#6 Write a Python program to replace all occurrences of space, comma, or dot with a colon.
s = re.sub(r',|\.|\s', r':', n)
print(s)

#7 Write a python program to convert snake case string to camel case string.
camel = re.sub(r'_([a-z])', lambda m: m.group(1).upper(), n)
print(camel)

#8 Write a Python program to split a string at uppercase letters.
s = re.split(r"[A-Z]", n)
for i in s: print(i, end=" ")
# s = re.findall(r'[A-Z][^A-Z]*', n)
# for i in s: print(i, end=" ")
print('\n')

#9 Write a Python program to insert spaces between words starting with capital letters.
spa = re.sub(r'(?<!^)(?=[A-Z])', ' ', n)
print(spa)

#10 Write a Python program to convert a given camel case string to snake case.
snake = re.sub(r'(?<!^)(?=[A-Z])', '_', n).lower()
print(snake)