list = [5, 4, 3, 2, 1]

for i in range(len(list)):
    min_idx = i
    for j in range(i+1, len(list)):
        if list[j] < list[i]:
            min_idx = j

    min = list[min_idx]
    list[min_idx] = list[i]
    list[i] = min

print(list)