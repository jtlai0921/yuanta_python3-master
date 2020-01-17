import random

iMax, iMin = 100, 0
iTarget = random.randint(iMin, iMax)


def check(iGuess, iMin, iMax):
    if iGuess == iTarget:
        # print("Good")
        return True, iMin, iMax
    elif iGuess > iTarget:
        iMax = iGuess
        # print("{0}~{1}".format(iMin, iMax))
        return False, iMin, iMax
    else:
        iMin = iGuess
        # print("{0}~{1}".format(iMin, iMax))
        return False, iMin, iMax


# print(iTarget)
while True:
    iGuess = int(input("{0}~{1} ->" .format(iMin, iMax)))
    if iGuess <= iMin or iGuess >= iMax:
        continue
    nResult, iMin, iMax = check(iGuess, iMin, iMax)
    if nResult:
        print("Good")
        break