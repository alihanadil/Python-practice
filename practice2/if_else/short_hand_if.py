#If you have only one statement to execute, you can put it on the same line as the if statement.
a = 5
b = 2
if a > b: print("a is greater than b")

#If you have one statement for if and one for else, you can put them on the same line using a conditional expression:
a = 2
b = 330
print("A") if a > b else print("B")

#You can chain conditional expressions, but keep it short so it stays readable:
a = 330
b = 330
print("A") if a > b else print("=") if a == b else print("B")