x = 987

a = abs(x)     # a = 987
temp = a % 10  # temp = 987 % 10 = 7
print(temp)

a = int(a/10)  # a = 987 / 10 = 98
temp = a % 10  # temp = 98 % 10 = 8
print(temp)

a = int(a/10)  # a = 98 / 10 = 9
temp = a % 10  # temp = 9 % 10 = 9
print(temp)

a = int(a/10)  # a = 9 / 10 = 0
temp = a % 10  # temp = 0 % 10 = 0
print(temp)
