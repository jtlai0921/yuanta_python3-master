import random

list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4

player = []
pc = []

def calc_sum():
    sum = 0.0
    for x in player:
        if x == 'A':
            sum += 1
        elif x == 'J' or x == 'Q' or x == 'K':
            sum += 0.5
        else:
            sum += int(x)

    return sum


random.shuffle(list)
# print(list)
while True:
    want = input('是否要牌?')
    if want == 'y':
        player.append(list.pop(0))
        sum = calc_sum()
        print(player, sum)
        if sum > 10.5:
            print('爆了')
            break
        elif sum == 10.5:
            print('YA~')
            break
    else:
        break

    if len(player) == 5:
        print('恭喜！過五關')
        break

# 與電腦 PK
player_sum = 0
pc_sum = 0
