class Celsius: # 攝氏
    def __get__(self, instance, owner):
        print("__get__")
        return 5 * (instance.fahrenheit - 32) / 9

    def __set__(self, instance, value):
        print("__set__")
        instance.fahrenheit = 32 + 9 * value / 5


class Temperature: # 溫度
    celsius = Celsius()

    def __init__(self, initial_f):
        print("__init__")
        self.fahrenheit = initial_f


t = Temperature(212)
print(t.celsius)
t.celsius = 0
print(t.fahrenheit)
