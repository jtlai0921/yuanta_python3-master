import random

balance = 1000
bet = 100


def dice_sum():
    dice = (1, 2, 3, 4, 5, 6)
    sum = 0
    for x in range(3):
        n = random.randint(0, 5)
        sum += dice[n]
        #print(n, dice[n], sum)
    return sum


while True:
    ans = dice_sum()
    guess = input('猜大(b)小(s)不玩(0) balance=$%d ? ' % balance)
    if guess == '0':
        break;
    elif guess == 'b' and ans >= 10:
        balance += bet
        print('答對了 ans=%d' % ans)
    elif guess == 's' and ans < 10:
        balance += bet
        print('答對了 ans=%d' % ans)
    else:
        balance -= bet
        print('答錯了 ans=%d' % ans)
