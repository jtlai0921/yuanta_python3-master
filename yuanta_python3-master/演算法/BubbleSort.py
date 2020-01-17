list = [5, 4, 3, 2, 1]

for i in range(len(list)):
    for j in range(len(list) - 1):
        print(i, list)
        if list[j] > list[j + 1]:
            max = list[j]
            list[j] = list[j + 1]
            list[j+1] = max



