class A :
    def __new__(cls):
        print("__new__ ")
        return super(A, cls).__new__(cls)  # 手動方式正確創建實例

    def __init__(self):
        print("__init__ ")
        super(A, self).__init__()

    def __call__(self):
        print("__call__ ")

a = A()
a2 = A()
a()
a2()