import random

lotto = set()
while len(lotto) < 5:
    #i = random.randrange(1, 40) # 1 <= i < 40
    i = random.randint(1, 39) # 1 <= i <= 39
    lotto.add(i)

print(lotto)
