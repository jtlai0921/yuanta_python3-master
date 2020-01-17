list = [5, 4, 3, 2, 1]

for i in range(1, len(list)): #第一個元素固定，從第二個開始
    tmp = list[i]
    j = i - 1 # 固定元素的前一個數字
    while j >= 0 and tmp < list[j]:
        list[j + 1] = list[j] # 值向右
        j = j - 1
    list[ j + 1 ] = tmp
    print("pass", i, ": ", list)

print(list)