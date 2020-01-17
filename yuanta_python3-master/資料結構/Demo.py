# Python 基本資料結構
# list 列表（資料可重複）
# tuple 列表(唯讀)
# dict 字典（key/value）
# set 集合（資料不重複）

# list 列表（資料可重複）
scores = [100, 90, 90, 80] * 3
scores[1] = 95
scores.append(70)
print(scores)

# tuple 列表(唯讀)
scores = (100, 90, 90, 80)
#tuple[1] = 95
#tuple.append(70)
print(scores)

# list 與 tuple 互轉
scores = list((100, 90, 90, 80))
print(scores)
scores = tuple([100, 90, 90, 80])
print(scores)

# dict 字典（key/value）
scores = {'國文':100, '數學':95, '英文':70, '歷史':58}
print(scores)
print(scores.get('國文'))
print(scores.values())
print(scores.keys())

# 使用「函式update」合併兩個字典
scores1 = {'國文':100, '數學':95}
scores2 = {'英文':70, '歷史':58}
scores1.update(scores2)
print(scores1)

#將 tuple 或串列轉換成字典
a1 = [
        ['國文', 100],
        ['數學', 95],
        ['英文', 90],
        ['歷史', 58],
    ]
print(dict(a1))

# 集合(set)儲存沒有順序性的資料，要找出資料是否存在，集合內元素不能重複
s = set([100, 90, 90, 80])
print(s)
s = set((100, 90, 90, 80))
print(s)

# dict 轉 set 集合
s = set({'國文':100, '數學':95, '英文':70, '歷史':58, '歷史':58})
print(s) # 只存放 key 值
