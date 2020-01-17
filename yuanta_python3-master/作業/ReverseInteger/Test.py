x = 987

a = abs(x)

# temp = a % 10
# print(temp)
#
# a = int(a/10)
# temp = a % 10
# print(temp)
#
# a = int(a/10)
# temp = a % 10
# print(temp)
#
# a = int(a/10)
# temp = a % 10
# print(temp)

num = 0
while a != 0:
    temp = a % 10
    num = num * 10 + temp
    print(temp)
    a = int(a / 10)

print(num)