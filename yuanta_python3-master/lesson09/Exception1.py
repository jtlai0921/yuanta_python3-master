a = 100
b = 0

try:
    c = a / b
except (ZeroDivisionError, IndexError) as value:
    print(value)
else:
    print(c)
finally:
    print('must be done')
