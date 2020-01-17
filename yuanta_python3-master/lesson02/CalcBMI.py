import random
import math
print('BMI計算')
h = 170.531
w = random.randint(40, 80)
bmi = w / (h/100)**2
bmi = w / math.pow(h/100, 2)
print("%.2f" % bmi)
print("{0:.2f}".format(bmi))


print('h=' + str(h) + ", w=" + str(w))
print(h, w, sep='&', end='\t')
print(h, w, sep="&")
print("h=%.2f w=%03d" % (h, w))
print("h={0} w={1}".format(h, w))
print("h={0:.2f} w={1}".format(h, w))

