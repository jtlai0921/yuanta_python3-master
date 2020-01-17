def calc(h, w):
    bmi = w / (h/100)**2
    msg = ''
    print('bmi=%.2f' % bmi)
    if 18 <= bmi < 23:
        msg = '正常'
    elif bmi >= 23:
        msg = '過胖'
    else:
        msg = '過瘦'

    return bmi, msg


h = float(input('請輸入身高:'))
w = float(input('請輸入體重:'))
print(h, w)
bmi, msg = calc(h, w)
print(bmi, msg)
