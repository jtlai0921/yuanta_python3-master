# 有1、2、3、4個數字，能組成多少個互不相同且無重複數字的三位數？
for i in range(1, 5):
    for j in range(1, 5):
        for k in range(1, 5):
            if i != j and j != k:
                print(i, j, k)


