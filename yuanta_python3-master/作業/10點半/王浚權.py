import random

def calc_sum(person):
    sum = 0.0
    for x in person:
        if x == 'A':
            sum += 1
        elif x == 'J' or x == 'Q' or x == 'K':
            sum += 0.5
        else:
            sum += int(x)

    return sum


def DoPlayer():

    while True:
        player.append(list.pop(0))
        player_sum = calc_sum(player)
        print("Player Poker: {0}, Sum: {1}".format(player, player_sum))
        if player_sum > 10.5:
            print('爆了!')
            break
        elif player_sum == 10.5:
            print('10點半!')
            break

        if len(player) == 5:
            print('過五關!')
            break

        want = input('是否要牌?')
        if want != 'y':
            break

    return player_sum

def DoPC():

    while True:
        pc.append(list.pop(0))
        pc_sum = calc_sum(pc)

        if pc_sum >= 9:
            break

        count1 = list.count('A')
        count2 = list.count('2')
        count3 = list.count('3')

        count_sum7 = count1 + count2 + count3
        count_sum8 = count1 + count2

        if pc_sum >= 7 and pc_sum <= 7.5 and count_sum7 < 12:
            break
        elif pc_sum >= 8 and pc_sum <= 8.5 and count_sum8 < 10:
            break

    print("PC Poker: {0}, Sum: {1}".format(pc, pc_sum))
    return pc_sum

#entry point
player_money = 100

while True:
    player = []
    pc = []
    list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
    random.shuffle(list)
    # print(list)

    print("玩家現金: {0}".format(player_money))

    player_bid = int(input('下注金額(輸入 0 結束):'))

    if player_bid == 0:
        break

    if player_bid > player_money:
        print('金額不足')
        break

    player_sum = DoPlayer()
    pc_sum = DoPC()

    if player_sum == 10.5 and len(player) == 2:
        player_money = player_money + player_bid
        print('玩家十點半獲勝')
    elif player_sum <= 10.5 and len(player) == 5:
        player_money = player_money + player_bid
        print('玩家過五關獲勝')
    elif player_sum == 10.5 and len(player) > 2 and pc_sum == 10.5 and len(pc) > 2:
        player_money = player_money + player_bid
        print('都十點半，玩家獲勝')
    elif player_sum > 10.5 and pc_sum > 10.5:
        print('兩邊都暴，平手')
    elif player_sum <= 10.5 and pc_sum > 10.5:
        player_money = player_money + player_bid
        print('電腦暴了，玩家獲勝')
    elif player_sum > 10.5 and pc_sum <= 10.5:
        player_money = player_money - player_bid
        print('玩家暴了，電腦獲勝')
    elif player_sum > pc_sum:
        player_money = player_money + player_bid
        print('玩家獲勝')
    elif player_sum < pc_sum:
        player_money = player_money - player_bid
        print('電腦獲勝')
    else:
        print('點數相同，平手')
