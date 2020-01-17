class Account:
    name = '' # 公有屬性
    __balance = 0 # 私有屬性

    def __init__(self, name, __balance):
        self.name = name
        self.__balance = __balance

    def setBalance(self, balance): # 物件方法，需含 self 參數
        self.__balance = balance

    def getBalance(self):
        return self.__balance


account = Account('John', 10000)
print(account.name, account.getBalance())