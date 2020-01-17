# 裝飾模式應用
def divide_decorated(func):
    def inner(a,b):
        if b == 0:
            return
        return func(a,b)
    return inner

@divide_decorated
def divide(a,b):
    return a/b

print(divide(2,5))
print(divide(2,0))
