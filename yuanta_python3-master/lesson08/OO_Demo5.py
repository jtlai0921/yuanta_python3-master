class Account:
    name = '' # 公有屬性
    __balance = 0 # 私有屬性

    def __init__(self, name:str=None, __balance:int=None):
        self.name = name
        self.__balance = __balance

a = Account('John', 100)
b = Account(100)
c = Account()
