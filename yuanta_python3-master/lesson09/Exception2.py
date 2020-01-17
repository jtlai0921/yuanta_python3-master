def calc(a, b):
    if b == 0:
        raise Exception('b is zero')
    print(a/b)


try:
    calc(10, 0)
except Exception as e:
    print(e);
