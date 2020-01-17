import random
lotto = set()
while len(lotto) < 5:
    num = random.randint(1, 40)
    lotto.add(num)

print(lotto)
print(len(lotto))
