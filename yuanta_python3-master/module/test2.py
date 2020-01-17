class A:
    def __new__(cls):
        print("__new__ ")
        return super(A, cls).__new__(cls) # 手動方式正確創建實例

    def __init__(self):
        print("__init__ ")
        super(A, self).__init__()

    def __call__(self):
        print('__call__ ')

a = A()
a()

class B:
    def __new__(cls, *args, **kwargs):
        print("__new__", args, kwargs)
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        print("__init__", args, kwargs)


B(1, 2, 3)

