# 參數篇
def calc(x, y):
    print(str(x+y))


def calc(x, y=None):
    if(y == None):
        print(str(x*2))
    else:
        print(str(x + y))


calc(10)
calc(10, 20)


def print_sum(*score):
    print(type(score))
    print(sum(score))


def print_sum2(a, *score, **kwargs):
    print(type(a))
    print(type(score))
    print(type(kwargs))
    print(a)
    print(score)
    print(kwargs)


print_sum2(10, 20, k=1, k2=2)

x = 0


# 全域變數
def update_x():
    global x
    x = 100  #  區域變數


update_x()
print(x)


# 高階函式
def add(x):
    return x + 1


def sub(x):
    return x - 1


def oper(func, x):
    return func(x)


print(oper(add, 10))
print(oper(sub, 10))


# 嵌套函式
def add(n1):
    def func(n2):
        return n1 + n2
    return func

print(add(1)(2))  # 顯示 3


# 裝飾模式
def make_pretty(func):
    def inner():
        print("戴帽子")
        func()
    return inner


def make_pretty2(func):
    def inner():
        print("紮S腰帶")
        func()
    return inner


def make_pretty3(func):
    def inner():
        print("帶水壺")
        func()
    return inner


@make_pretty
@make_pretty2
@make_pretty3
def soldier():
    print("阿兵哥")

soldier()
