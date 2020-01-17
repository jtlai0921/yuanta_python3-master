'''
[
      [1],
    [1, 1],
   [1, 2, 1],
  [1, 3, 3, 1],
[1, 4, 6, 4, 1]
]

print(result[列][行])
print(result[2][1]) --> 2
'''
def gen(n):
    result = []
    for i in range(n):
        result.append([])
        for j in range(i+1):
            if j in (0, i):
                result[i].append(1)
            else:
                result[i].append(result[i-1][j-1] + result[i-1][j])
                #result[i].append(0)
                pass

    return result

print(gen(5))


