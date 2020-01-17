import random

pPokerCards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'J', 'Q', 'K'] * 4

random.shuffle(pPokerCards)

pManCards = []
pPCCards = []
dManScore = -1
dPCScore = -1


def computeScore(pCards):
    dScore = 0
    for pCard in pCards:
        if pCard == 'A':
            dScore += 1
        elif pCard == 'J' or pCard == 'Q' or pCard == 'K':
            dScore += .5
        else:
            dScore += int(pCard)
    return dScore


def pcThink(dScore):
    if dScore <= 6:
        return True
    elif dScore >= 9:
        return False
    elif dScore < 8:
        if pPokerCards.count('A') + pPokerCards.count('1') + pPokerCards.count('2') + pPokerCards.count('3') >= 12:
            return True
        else:
            return False
    else:
        if pPokerCards.count('A') + pPokerCards.count('1') + pPokerCards.count('2') >= 10:
            return True
        else:
            return False


print("\n  --==玩家先==--  \n")
pManCards.append(pPokerCards.pop(0))
dManScore = computeScore(pManCards)
print("玩家的牌 %s %.1f" % (pManCards, dManScore))
ans = input("要補牌嗎? (y/n) ==> ")
nWantCard = (ans == 'y' or ans == 'Y')
while nWantCard:
    pManCards.append(pPokerCards.pop(0))
    dManScore = computeScore(pManCards)
    print("玩家的牌 %s %.1f" % (pManCards, dManScore))
    if dManScore > 10.5:
        print("爆了")
        break
    elif len(pManCards) == 5:
        print("過五關")
        break
    elif dManScore == 10.5:
        print("十點半")
        break
    else:
        ans = input("要補牌嗎? (y/n) ==> ")
        nWantCard = (ans == 'y' or ans == 'Y')


if dManScore <= 10.5 and len(pManCards) < 5:
    print("\n  --==換莊家==--  \n")
    pPCCards.append(pPokerCards.pop(0))
    dPCScore = computeScore(pPCCards)
    print("莊家的牌 %s %.1f" % (pPCCards, dPCScore))
    nWantCard = pcThink(dPCScore)
    print("要補牌嗎? (y/n) ==> %s" % ('y' if nWantCard else 'n'))
    while nWantCard:
        pPCCards.append(pPokerCards.pop(0))
        dPCScore = computeScore(pPCCards)
        print("莊家的牌 %s %.1f" % (pPCCards, dPCScore))
        if dPCScore > 10.5:
            print("爆了")
            break
        elif len(pPCCards) == 5:
            print("過五關")
            break
        elif dPCScore == 10.5:
            print("十點半")
            break
        else:
            nWantCard = pcThink(dPCScore)
            print("要補牌嗎? (y/n) ==> %s" % ('y' if nWantCard else 'n'))

print("\n")
if dManScore > 10.5 or dPCScore <= 10.5 and len(pPCCards) == 5:
    print("莊家贏了")
elif dPCScore <= 10.5 and dManScore <= 10.5:
    if dManScore > dPCScore:
        print("玩家贏了")
    elif dManScore < dPCScore:
        print("莊家贏了")
    else:
        print("雙方平手")
elif dPCScore > 10.5:
    print("玩家贏了")