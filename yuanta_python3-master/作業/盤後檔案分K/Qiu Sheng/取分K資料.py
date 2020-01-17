# ticks.txt 下載
# https://drive.google.com/open?id=1mi9_MCgz-l3YOOCQGgy4mHiyMKFjhSN1
# 取得分 K 資料
# 1100, 10704, 10713, 10749, 10682, 59806
# 1101, 10704, 10713, 10749, 10682, 60126
# ...
# 1115, 10703, 10713, 10749, 10682, 62372
# 存放到 sqlite 中
# 資料表名 TX
# 欄位:
# ReqType, MatchTime, MatchPri, OpenPri,
# HighPri, LowPri, TolMatchQty

import sqlite3
import os

class MinTick:
    regtype = 0
    time = ''
    open_price = 0
    high_price = 0
    low_price = 0
    match_price = 0
    match_qty = 0

def UpdateTickDataToDB(mintick):
    # region UpdateTickDataToDB
    conn = sqlite3.connect('homework.db')
    cursor = conn.cursor()  # 建立 cursor

    sql = ('INSERT OR REPLACE INTO TX(ReqType, MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty) '
                   'VALUES (%s,%s,%s,%s,%s,%s,%d)' %
                   (mintick.regtype,
                    mintick.time,
                    mintick.match_price,
                    mintick.open_price,
                    mintick.high_price,
                    mintick.low_price,
                    mintick.match_qty))

    cursor.execute(sql)
    conn.commit()  # 執行資料庫更新
    conn.close()
    print('更新成功')
    # endregion

# 讀檔
file = open('ticks.txt', 'r', encoding='utf-8')
filedatas = file.read()


list = filedatas.split('\n')
i = 1  # 第一項是沒用的資料
dic_MinTicks = {}
pre_time = ''

while i < len(list):
    # region while i < len(list):
    # print(list[i])
    data = list[i].split(',')
    regtype = data[0] # strip去空白
    time = data[1].strip()[:4] # 時間只取前四碼
    match_price = data[2].strip()
    open_price = data[3].strip()
    high_price = data[4].strip()
    low_price = data[5].strip()
    match_qty = int(data[6].strip())
    mt = MinTick()

    # region 找出分K資料
    if time not in dic_MinTicks.keys():
        # 換分 把前一分的分K資料更新上去
        if pre_time != '':
            UpdateTickDataToDB(dic_MinTicks[pre_time])
        mt.regtype = regtype
        mt.time = time
        mt.open_price = open_price
        mt.high_price = high_price
        mt.low_price = low_price
        mt.match_price = match_price
        mt.match_qty = match_qty
    else:
        mt = dic_MinTicks[time]

    pre_time = time
    # endregion

    # region 分K資料更新
    if mt.high_price < high_price:
        mt.high_price = high_price
    if mt.low_price > low_price:
        mt.low_price = low_price

    mt.match_price = match_price
    mt.match_qty = match_qty
    # endregion

    # 更新進字典檔
    dic_MinTicks[str(mt.time)] = mt

    # 每個tick更新
    # UpdateTickDataToDB(mt)

    i = i + 1
    # endregion

# 更新最後一個分K
if time != '':
    UpdateTickDataToDB(dic_MinTicks[time])
