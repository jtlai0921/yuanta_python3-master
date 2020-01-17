class Report(object):

    class DB:
        def __init__(self):
            self.val = 'empty'
        def __str__(self):
            return 'self:' + self.val
    instance = None

    def __new__(cls): # __new__ always a classmethod
        if not Report.instance:
            Report.instance = Report.DB()
        return Report.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

x = Report()
print(x)

a = Report()
a.val = 'mysql'
print(a)

b = Report()
b.val = 'derby'
print(b)

c = Report()
c.val = 'oracle'
print(c)

print('----------------')
print(a, b, c)