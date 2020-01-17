a = 100
b = 0

try:
    c = a / b
except BaseException as e:
    print(type(e).__name__)
    print(e.args)
else:
    print(c)

