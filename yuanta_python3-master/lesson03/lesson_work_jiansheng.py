import random

range_start = 0
range_end = 100
ans = random.randint(range_start+1, range_end-1)

while True:
    inpu = int(input("%d~%d -> " % (range_start, range_end)))
    if(ans == inpu):
        print("OK")
        break
    elif(inpu < range_start or inpu > range_end):
        continue
    elif(inpu > ans):
        range_end = inpu
    elif(inpu < ans):
        range_start = inpu