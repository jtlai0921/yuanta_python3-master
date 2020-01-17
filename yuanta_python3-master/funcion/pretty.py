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
