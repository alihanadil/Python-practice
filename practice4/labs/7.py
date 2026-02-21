class Reverse:
    def __init__(self, word):
        self.word = word
    def __iter__(self):
        self.a = -1
        return self
    def __next__(self):
        if self.a >=-len(self.word):
            x = self.word[self.a]
            self.a -=1
            return x
        else: raise StopIteration
myiter = iter(Reverse(input()))
for i in myiter: print(i,end="")