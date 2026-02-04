#Methods are functions that belong to a class. They define the behavior of objects created from the class.
class Person:
  def __init__(self, name):
    self.name = name

  def greet(self):
    print("Hello, my name is " + self.name)

p1 = Person("Emil")
p1.greet() 
#Note: All methods must have self as the first parameter.
