# -*- coding: utf-8 -*-
# Author: 元大證券資訊部溫鳳祥
import random

list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4

player = []
pc = []

def calc_sum(cards):
    sum = 0.0
    for x in cards:
        if x == 'A':
            sum += 1
        # elif x == 'J' or x == 'Q' or x == 'K':
        elif x in ('J', 'Q', 'K'):
            sum += 0.5
        else:
            sum += int(x)
    return sum

def calc_sum_remain():
    sum = 0.0
    for x in list:
        if x == 'A':
            sum += 1
        elif x in [ '2', '3' ]:
            sum += int(x)
    return sum

def check_winner():
    winner = None
    sum_player = calc_sum(player)
    sum_pc = calc_sum(pc)
    if sum_player > 10.5:
        print('玩家爆掉...輸牌')
        winner = 'pc'
    elif sum_pc > 10.5:
        print('莊家爆掉...輸牌')
        winner = 'player'
    elif sum_player == 10.5:
        if len(player) == 5:
            if sum_player == 10.5:
                print('恭喜！玩家過五關且點數 = 10.5，贏牌！')
                winner = 'player'
        elif len(pc) == 5:
            print('莊家過五關，贏牌！')
            winner = 'pc'
    else:   # sum_player < 10.5
        if len(player) == 5:
            print('恭喜！玩家過五關，贏牌！')
            winner = 'player'
        elif sum_pc <= 10.5 and len(pc) == 5:
            print('莊家過五關且點數 <= 10.5，贏牌！')
            winner = 'pc'
        # elif sum_pc < 10.5:
        #     if sum_player > sum_pc:
        #         print('恭喜！玩家贏牌！')
        #         winner = 'player'
        #     else:
        #         print('莊家贏牌！')
        #         winner = 'pc'

    print('玩家牌組：', player, ' sum =', sum_player)
    print('莊家牌組：', pc, ' sum =', sum_pc)
    return winner

# 與電腦 PK
player_sum = 0
pc_sum = 0
random.shuffle(list)
print('All cards: ', list)
while True:
    want = input('是否要牌: ')
    if want == 'y':
        player.append(list.pop(0))
    else:
        print('玩家 pass')

    if check_winner() != None:
        break

    sum = calc_sum(pc)
    sum_remain = calc_sum_remain()
    if sum >= 9:
        print('莊家 pass')
    elif (sum == 7 or sum == 7.5) and sum_remain >= 12:
        print('莊家要牌')
        pc.append(list.pop(0))
    elif (sum == 8 or sum == 8.5) and sum_remain >= 10:
        print('莊家要牌')
        pc.append(list.pop(0))
    else:
        print('莊家要牌')
        pc.append(list.pop(0))

    if check_winner() != None:
        break
