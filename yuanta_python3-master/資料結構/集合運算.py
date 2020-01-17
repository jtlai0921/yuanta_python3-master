# 集合的運算
# 聯集(|)、交集(&)、差集(-)與互斥或(^)運算。
# 聯集(|)
a = set('12345')
b = set('24680')
print(a, b)
print('聯集(|)', a | b)
# 交集(&)
print('交集(&)', a & b)
# 差集(-)
print('差集(-)', a - b)   # 集合A減去集合B的元素。
#互斥或(^)運算
print('互斥或(^)', a ^ b) # 元素存在集合A，但不存在集合B。

# 集合的比較
# 可以將任兩個集合進行子集合(<=)、真子集合(<)、超集合(>=)與真超集合(>)等四個比較運算
a = set('135')
b = set('12345')
print(a <= b) # 存在集合A的每個元素，也一定存在於集合B，則回傳True。
print(a.issubset(b))
print('a < b', a < b) # 存在集合A的每個元素，也一定存在於集合B，且集合B至少有一個元素不存在於集合A，則回傳True。
print(a >= b) # 存在集合B的每個元素，也一定存在於集合A，則回傳True。
print(a.issuperset(b))
print(a > b) # 存在集合B的每個元素，也一定存在於集合A，且集合A至少有一個元素不存在於集合B，則回傳True。

# difference 共同元素去除
a = set('135')
b = set('12345')
c = b.difference(a) # {'4', '2'} a 與 b 共同元素去除
print(c)

# intersection 只取共同元素
a = set('135')
b = set('12345')
c = a.intersection(b) # {'1', '5', '3'} 只取 a 與 b 共同元素
print(c)

# 判断 2 集合否有包含相同元素，若有 False，沒有 True：
x = set('135')
y = set('246')
z = x.isdisjoint(y)
print(z)

# 返回两个集合中不重复的元素集合，即会移除两个集合中都存在的元素。
x = set('13')
y = set('23')
z = x.symmetric_difference(y)
print(x, y, z)

x = set('13')
y = set('23')
x.symmetric_difference_update(y)
print(x)