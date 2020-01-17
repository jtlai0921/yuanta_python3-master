import  random
poker = ['A', '2', '3', '4', '5', '6','7', '8', '9', '10', 'J', 'Q', 'K']
king = []#莊家點數
poker = poker * 4
random.shuffle(poker) #洗牌
player = [] #玩家點數
money = 100 #錢
gamenum = 0 #局數
keepmoney = 0 #下注金額

#計算點數
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

def calc_kingsum():
    sum = 0.0
    for x in king:
        if x == 'A':
            sum += 1
        elif x == 'J' or x == 'Q' or x == 'K':
            sum += 0.5
        else:
            sum += int(x)
    print("莊家為%s " % sum)
    return sum


def calc_kingadd(kingrnum):
    while True:
        if (kingrnum <= 6):
            king.append(poker.pop(0))
            kingrnum = calc_kingsum()
        elif (6 < kingrnum <= 7.5):
            if (poker.count('A')+poker.count( '1')+poker.count( '2')+poker.count( '3') >= 12):
                king.append(poker.pop(0))
                kingrnum = calc_kingsum()
            else:
                break;
        elif (7.5 < kingrnum <= 8.5):
            if (poker.count('A')+poker.count( '1')+poker.count( '2') >= 10):
                king.append(poker.pop(0))
                kingrnum = calc_kingsum()
            else:
                break;
        else:
            break;

    return kingrnum

while True:
     gamenum+=1
     if(money <= 0):
         print("金額%s結束遊戲" % money)
     else:
         q1 = input("第%s局金額%s是否遊玩(Y/N)" %(gamenum, money))
         if(q1 == 'y' or q1 == 'Y'):
             king = []  # 莊家點數
             player = []  # 玩家點數
             keepmoney = int(input("下注金額為："))
             #玩家第1張
             player.append(poker.pop(0))
             playernum = calc_sum()
             #莊家第1張
             king.append(poker.pop(0))
             kingrnum = calc_kingsum()
             while True:
                 s1 = input('玩家%s點是否要牌？' % playernum)
                 if(s1 == 'y' or s1 == 'Y'):
                     player.append(poker.pop(0))
                     playernum = calc_sum()
                     if(int(playernum) > 10.5):
                         print("玩家%s點輸了" % playernum)
                         money = money - keepmoney
                         break;
                     if(len(player) >= 5):
                         print('玩家過五關!')
                         money = money + keepmoney * 2
                         break
                 else:
                     #計算莊家要牌和點數
                     kingrnum = calc_kingadd(kingrnum)
                     print("比較雙方牌組：莊家為%s  玩家%s" % (kingrnum ,playernum))
                     if(kingrnum>10.5 or playernum > kingrnum):
                         print("玩家贏了")
                         money = money + keepmoney
                         break
                     elif(len(king) > 5 or kingrnum > playernum):
                         print("玩家輸了")
                         money = money - keepmoney
                         break
                     else:
                         print("雙方平手")
                         break


