class Book(object):
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def __str__(self):
        return self.name + ' cost : ' + str(self.value)


c = Book()
c.name = 'Python'
c.value = 180
print(c.name, c.value)