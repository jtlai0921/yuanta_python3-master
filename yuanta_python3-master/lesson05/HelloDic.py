dic = {'orange':20, 'apple':100}
print(dic)
dic['banana'] = 50
print(dic)
print(dic.get('orange'))
print(dic.get('berry', 70))
print(dic)
print(dic.setdefault('berry', 70))
print(dic)
