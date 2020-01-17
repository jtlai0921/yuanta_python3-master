f2 = lambda: print('ok')
f2()

f = lambda x, y : x if x > y else y
print(f(10, 20))

def max(x, y):
    return x if x > y else y

f3 = lambda x, y : max(x, y)
print(f3(10, 20))

print({'A':100, 'B':80}.get('A', None))

{'1':lambda: print('男'), '2':lambda: print('女')}.get('2', None)()
