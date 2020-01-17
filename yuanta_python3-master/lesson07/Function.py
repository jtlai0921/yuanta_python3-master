# 自訂函式
def print_args(first, *args, **kwargs):
    print(first)
    print(args)
    print(kwargs)


print_args('a', 1, 2, 3, h=170, w=60)

# 自訂函式 Lab
def ctof(c):
    return c*(9/5)+32


def ftoc(f):
    return (f-32)*5/9


print(ctof(10))
print(ftoc(50))

# 高階函式
def add(x):
    return x + 1

def sub(x):
    return x - 1

def oper(func, x):
    return func(x)

print(oper(sub, 5))

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

@make_pretty
@make_pretty2
def soldier():
    print("阿兵哥")

soldier()


#Lambda

f = lambda x:x*x - x
print(f(3))

def calc(x):
    return x**2

b = lambda x : calc(x)
print(b(10))


max = lambda x, y : x if x>y else y
print(max(10, 20))


#switch lambda
id = 'A223456789'
sex = id[1]
{
    '1':lambda : print('男'),
    '2':lambda : print('女'),
}.get(sex, lambda :print('性別錯誤'))()

