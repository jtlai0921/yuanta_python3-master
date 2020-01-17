import random
poker = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
poker = poker*4
random.shuffle(poker)

player1 = []
player2 = []

def Cal_Card(player):
    num = 0
    for card in player:
        if card == 'A':
            num = num + 1
        elif card == 'J' or card == 'Q' or card == 'K':
            num = num + 0.5
        else:
            num = num+ int(card)
    return num;

def Status_Judge(player, num):
    if(num > 10.5):
        print('爆了')
        return False
    elif(num == 10.5):
        print('恭喜 十點半')
        return False
    elif(num < 10.5 and len(player1) == 5):
        print('恭喜 過五關')
        return False
    return True

num1=0
while True:
    getnext = input("是否要牌? Y/N  ")
    if(getnext == 'N'):
        break
    else:
        player1.append(poker.pop(0))
        num1 = Cal_Card(player1)

    print("{0}, {1}".format(player1, num1))
    if(Status_Judge(player1, num1) == False):
        break

print("莊家回合")
num2=0
while True:
    #getnext = input("是否要牌? Y/N  ")

    if(num2 <= 6): # 不足6點強迫補牌
        getnext = 'Y'
    elif(num2 >= 9): # 9點以上不須補牌
        getnext = 'N'
    elif(num2 == 7 or num2 == 7.5): # 7或7.5看A、2、3剩餘牌數 >=12補
        if(poker.count('A')+poker.count('2')+poker.count('3') >= 12):
            getnext = 'Y'
        else:
            getnext = 'N'
    elif(num2 == 8 or num2 == 8.5): # 8或8.5看A、2剩餘牌數 >=10補
        if(poker.count('A')+poker.count('2') >= 10):
            getnext = 'Y'
        else:
            getnext = 'N'

    if(getnext == 'N'):
        break
    else:
        player2.append(poker.pop(0))
        num2 = Cal_Card(player2)

    print("{0}, {1}".format(player2, num2))
    if (Status_Judge(player1, num2) == False):
        break

if(num1 > 10.5) :
    num1 = 0
if(num2 > 10.5) :
    num2 = 0

if(num1 > num2):
    print("玩家獲勝")
elif(num1 == num2):
    if(len(player1) > len(player2)):
        print("玩家獲勝")
    else:
        print("莊家獲勝")
else:
    print("莊家獲勝")