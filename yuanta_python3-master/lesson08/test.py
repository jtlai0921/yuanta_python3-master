from lesson08 import *

print(os.name)
print(sys.platform)

print(random()) # 0 <= n < 1.0
print(randint(1, 10)) # 1 <= n <= 10
print(randrange(1, 10)) # 1 <= n < 10
lan = ["Java", "Python", "C#", "Swift"]
print(choice(lan)) # 任取一字串
shuffle(lan) # 洗牌
print(lan)

copyright()
