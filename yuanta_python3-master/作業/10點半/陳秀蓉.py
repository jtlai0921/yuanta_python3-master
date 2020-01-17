import random
poker = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

poker = poker * 4
random.shuffle(poker)
mypoker = []
pcpoker = []
mymoney = 100
pcmoney = 100

def SumDot(cpoker):
    pdot = 0.0
    for i in cpoker:
        if (i=="J" or i=="Q" or i=="K"):
            pdot += 0.5
        elif ( i=="A" ):
            pdot += 1
        else:
            pdot += int(i)
    return pdot

def ChkPcg(sdot):
    bchk=True
    if (sdot >= 9):
        bchk=False
    elif (sdot >= 7 and sdot < 9):
        ac= pcpoker.count("A")
        c1= pcpoker.count("1")
        c2= pcpoker.count("2")
        c3= pcpoker.count("3")
        if (sdot == 7 or sdot == 7.5):
            if ((ac + c1 + c2 +c3) < 12):
                bchk=False
                # print("檢查A,1,2,3剩餘牌數<12(不補)")
        elif (sdot == 8 or sdot == 8.5):
            if ((ac+c1+c2)<10):
                bchk=False
                # print("檢查A,1,2剩餘牌數<10(不補)")

    return bchk

def GetPoker(pk):
    k = len(poker)
    i = random.randint(0, k)
    print(poker[i])
    pk.append(poker.pop(i))

def CheckMoney(am):
    rb = False
    if (int(am)) > 100:
        print("投注金額不可超出100元")
        rb = True
    return rb


# print(poker)
pcdot=0.0
while True:
    ans = input("是否要牌?")
    if (ans=="y"):
        if ( mymoney==100 ):
            am = input("投注多少錢?")
            if (CheckMoney(am)):
                break
            pm = random.randint(1,100)
            summ = int(am) + pm
            mymoney -= int(am)
            pcmoney -= pm
        GetPoker(mypoker)
        sumdot = SumDot(mypoker)
        print("我的牌:%s 點數:%d" % (mypoker, sumdot))
        if (ChkPcg(pcdot)):
            GetPoker(pcpoker)
        pcdot = SumDot(pcpoker)
        # print("PC的牌:%s 點數:%d" % (pcpoker, pcdot))


        if (sumdot > 10.5 or pcdot > 10.5):
            if (sumdot) > 10.5:
                pcmoney += summ
            else:
                mymoney += summ
            print("爆點囉!! 我:%d PC:%d 你目前資金:%d 電腦資金:%d" % (sumdot, pcdot, mymoney, pcmoney))
            break
        elif (sumdot == 10.5 or pcdot == 10.5 ):
            if ( sumdot==10.5 ):
                mymoney += summ
            else:
                pcmoney += summ
            print("恭喜10點半!! 我:%d PC:%d  你目前資金:%d 電腦資金:%d" % (sumdot, pcdot, mymoney, pcmoney))
            break
    else:
        break

    if len(mypoker) == 5:
        mymoney += summ
        print('恭喜你！過五關,你目前資金:%d 電腦資金:%d' % (mymoney, pcmoney))
        break

    if len(pcpoker) == 5:
        pcmoney += summ
        print('恭喜pc！過五關,電腦資金:%d  你目前資金%d' % (pcmoney, mymoney))
        break


print("PC的牌:%s 點數:%d" % (pcpoker, pcdot))


