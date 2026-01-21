# 3 examples of expressions that will return boolean answer
print(10 > 9)
print(10 == 9)
print(10 < 9, "\n") 

#almost any value will equal to true
print (bool("abc"))
print(bool(123))
print(bool(["apple", "cherry", "banana"]), "\n")

#except for 0 and empty set, string, list, tuple
print(bool(False), bool(None), bool(0), bool(""),bool(()), bool([]), bool({}), sep="\n")