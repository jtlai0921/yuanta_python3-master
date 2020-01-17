def calc(x):
    return x*x-x


a = lambda x : x*x-x
print(a(10))


b = lambda x : calc(x)
print(b(10))


max = lambda x, y : x if x>y else y
print(max(10, 20))


#switch lambda
id = 'A223456789'
sex = id[1]
{
    '1':lambda : print('男'),
    '2':lambda : print('女'),
}.get(sex, lambda :print('性別錯誤'))()


