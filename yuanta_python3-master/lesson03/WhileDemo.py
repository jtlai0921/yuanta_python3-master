import random
x = 0
while True:
    x = random.randint(1, 9)
    if x % 2 == 0:
        print(x)
    else:
        break
