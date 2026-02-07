#When a class inherits from more than one base class, 
# it is called multiple inheritance. The derived class inherits all features of its base classes.
class Class1:
    def m(self):
        print("In Class1")

class Class2(Class1):
    def m(self):
        print("In Class2")
        super().m()

class Class3(Class1):
    def m(self):
        print("In Class3")
        super().m()

class Class4(Class2, Class3):
    def m(self):
        print("In Class4")   
        super().m()
     
print(Class4.mro())         
print(Class4.__mro__)