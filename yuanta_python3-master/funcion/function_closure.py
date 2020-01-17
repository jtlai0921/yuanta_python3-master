import time;


def calc_bmi(h, w):
    bmi = w/(h/100)**2
    def get_bmi():
        return bmi
    return get_bmi


bmi_a = calc_bmi(170, 60)
if 18 < bmi_a() < 23:
    print('good')
else:
    print('not good')
