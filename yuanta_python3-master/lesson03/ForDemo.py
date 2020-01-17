for i in range(1, 5):
    print(i)
# 1 2 3 4

for item in [10, 20, 30]:
    print(item)

for (i, item) in enumerate([10, 20, 30]):
    print(i, item)

hey = ["lol", "hey", "water", "pepsi", "jam"]
for item in hey:
    print(hey.index(item), item)

employees = {'Tom':70000, 'Mary':80000, 'John':55000}
for name in employees:
    print('%s 的薪資 %d' % (name, employees[name]))

for x in range(1, 2):
    print(x)
else:
    print('end')

for x in range(1, 2):
    pass

