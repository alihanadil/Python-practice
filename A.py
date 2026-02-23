class Book:
    def __init__ (self, title, author):
        self.title = title
        self.author = author
    def getInfo(self): print(f"{self.title} by {self.author}")
l = input().split()
a = Book(l[0],l[1])
a.getInfo()