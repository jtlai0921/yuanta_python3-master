def print_msg(msg):
    def printer():
        print(msg)
    printer()
    #return printer

print_msg('Hello')

# a = print_msg('Hello')
# a()

def add(x):
    def func(y):
        return x + y
    return func

print(add(10)(20))


def outer():
    x = 10
    def inner():
        print('x=', x)
    x = 20
    return inner

f = outer()
f()


def multi_of(n):
    print('n:', n)
    def multi(x):
        print('x:', x)
        return x * n
    return multi

#Multiplierof3
times3 = multi_of(3)

# times5 = multi_of(5)
#
print(times3(9))