#撲克牌遊戲十點半，人機對戰
#每人睹金100元，可自由下注
#電腦不足6點需強迫補牌，9點(含)以上不需補牌
#電腦若為7、8點則策略補牌
#若為7、7.5點，看A、2、3剩餘的牌>=12(補)
#若為8、8.5點，看A、2剩餘的牌>=10(補)

import random

poker = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
target = 10.5
player = []
pc = []
#點數
mysums = 0.0
pcsums = 0.0
#賭金
mybetall = 100
pcbetall = 100
#下注金額
mybet = 0
pcbet = 0

#計算點數
def calc_sum(tmparray):
    sums = 0.0
    for x in tmparray:
        if x == 'A':
            sums += float(1)
        elif x == 'J' or x == 'Q' or x == 'K':
            sums += 0.5
        else:
            sums += float(x)
    return sums

#發牌
def dealCard():
    num = random.randint(0, len(poker))
    cardTmp = poker[num]
    del poker[num]
    return cardTmp

#計算剩牌A、2、3
def calc_sum_rest(flg):
    sums = 0.0
    for x in poker:
        if x == 'A':
            sums += float(1)
        elif  x == '2' or (flg == "3" and x == '3'):
            sums += float(x)
        else:
            continue
    return sums

#電腦是否補牌
def isPCDealCard():
    rtnask = "n"
    sums = 0.0
    sums = calc_sum(pc)
    if sums < 6:
        rtnask = "y"
    elif sums < 8:
        if calc_sum_rest("3") >= 12:
            rtnask = "y"
    elif sums < 9:
        if calc_sum_rest("2") >= 10:
            rtnask = "y"
    return rtnask



while (mybetall > 0 and pcbetall > 0):

    myAsk = input("*** 是否要玩人機對帳10點半？y/n：")
    if myAsk != "y":
        print("結束")
        break

    print("您的賭金{0}，電腦的賭金{1}".format(mybetall, pcbetall))

    # 下注
    mybet = int(input("請您下注1~{0}：".format(mybetall)))
    while mybet <= 0 or mybet > 100:
        mybet = int(input("金額需大於0小於100，請您下注1~{0}：".format(mybetall)))

    #pcbet = random.randint(1, pcbetall)
    pcbet = mybet

    # 洗牌
    poker = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
    random.shuffle(poker)

    player = []
    pc = []

    myAsk = ""
    pcAsk = ""

    # 各發1張
    card = dealCard()
    player.append(card)
    print("您得一張牌：%s" % card)

    card = dealCard()
    pc.append(card)
    print("電腦得一張牌：%s" % card)


    while 1:
        if myAsk != "n":
            myAsk = input("您是否要牌？y/n")

        if myAsk == "y":
            card = dealCard()
            player.append(card)
            print("您得一張牌：%s" % card)
            #計算點數
            mysums = calc_sum(player)

            if mysums > target:
                print('您爆了 {0}，PC贏了'.format(mysums))
                mybetall = mybetall - pcbet
                pcbetall += pcbet
                break
            elif mysums == target:
                print('您贏了{0}'.format(mysums))
                mybetall += mybet
                pcbetall = pcbetall - mybet
                break

        if pcAsk != "n":
            pcAsk = isPCDealCard()

        if pcAsk == "y":
            card = dealCard()
            pc.append(card)
            print("電腦要牌：%s" % card)

            # 計算點數
            pcsums = calc_sum(pc)

            if pcsums > target:
                mybetall += mybet
                pcbetall = pcbetall - mybet
                print('電腦爆了 {0}，您贏了'.format(pcsums))
                break
            elif pcsums == target:
                mybetall = mybetall - pcbet
                pcbetall += pcbet
                print('電腦贏了{0}'.format(pcsums))
                break
        else:
            print("電腦不要牌了")

        #人機都不要牌
        if myAsk == "n" and pcAsk == "n":
            #計算點數
            mysums = calc_sum(player)
            print('您亮牌 {0}'.format(mysums))
            pcsums =  calc_sum(pc)
            print('您{0}，PC{1}'.format(mysums, pcsums))
            if mysums > pcsums:
                mybetall += mybet
                pcbetall = pcbetall - mybet
                print('您贏了')
                break
            elif mysums == pcsums:
                print('平手')
                break
            else:
                mybetall = mybetall - pcbet
                pcbetall += pcbet
                print('電腦贏了')
                break

    print("=> 您的牌：", player)
    print("=> 電腦的牌：", pc)
    print("=> 目前您的賭金{0}，電腦的賭金{1}".format(mybetall, pcbetall))