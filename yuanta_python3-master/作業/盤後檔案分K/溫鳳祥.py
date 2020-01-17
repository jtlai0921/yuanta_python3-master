# -*- coding: UTF-8 -*-
# Author: 元大證券資訊部溫鳳祥
# Desc: 從 tick.txt 取得分 K 資料，再存入 SQLite table "TX"

import sqlite3
import os

# read source file ticks.txt
curr_dir = os.path.dirname(os.path.realpath(__file__))
src_file = open('%s/ticks.txt' % curr_dir, mode='rt', encoding='UTF-8')

# create DB & table
conn = sqlite3.connect('ticks.db')
cursor = conn.cursor()
sql = '''CREATE TABLE IF NOT EXISTS TK (
ReqType INTEGER,
MatchTime INTEGER,
OpenPri INTEGER,
HighPri INTEGER,
LowPri INTEGER,
ClosePri INTEGER,
MatchQty INTEGER)'''
cursor.execute(sql)

# 計算分 K 資料
req_type = -1
match_hour = -1
match_min = -1
open_pri = -1
high_pri = -1
low_pri = -1
close_pri = -1
tol_match_qty = -1
tol_match_qty_prev = -1

src_file.readline().strip() # consume header
lines = src_file.readlines()
print("total lines=%d"%len(lines))
for ii in range(len(lines)):
    lines[ii] = lines[ii].strip()
    # print('[%d] line=%s' % (ii + 1, lines[ii]))
    values = lines[ii].replace(' ', '').split(',')
    req_type_tmp, match_hour_tmp, match_min_tmp = int(values[0]), int(values[1][0:2]), int(values[1][2:4])
    open_pri_tmp, high_pri_tmp, low_pri_tmp, close_pri_tmp = int(values[3]), int(values[4]), int(values[5]), int(values[2])
    tol_match_qty_tmp = int(values[6])
    if req_type != req_type_tmp or match_hour != match_hour_tmp or match_min != match_min_tmp:
        if req_type > -1 and match_hour > -1 and match_min > -1:
            sql = 'INSERT INTO TK (ReqType, MatchTime, OpenPri, HighPri, LowPri, ClosePri, MatchQty)'\
                ' VALUES(%d, %02d%02d, %d, %d, %d, %d, %d)'\
                % (req_type, match_hour, match_min, open_pri, high_pri, low_pri, close_pri, tol_match_qty - tol_match_qty_prev)
            cursor.execute(sql)
            conn.commit()
            print('[%05d] %s' % (ii + 1, sql))

            tol_match_qty_prev = tol_match_qty
            tol_match_qty = tol_match_qty_tmp
        else:   # first data item
            tol_match_qty = tol_match_qty_tmp
            tol_match_qty_prev = 0

        req_type = req_type_tmp
        match_hour = match_hour_tmp
        match_min = match_min_tmp
        open_pri = close_pri_tmp
        high_pri = close_pri_tmp
        low_pri = close_pri_tmp
        close_pri = close_pri_tmp

    else:   # same req_type & match_hour & match_min
        if high_pri < close_pri_tmp:
            high_pri = close_pri_tmp
        if low_pri > close_pri_tmp:
            low_pri = close_pri_tmp
        close_pri = close_pri_tmp
        tol_match_qty = tol_match_qty_tmp

# last data item
sql = 'INSERT INTO TK (ReqType, MatchTime, OpenPri, HighPri, LowPri, ClosePri, MatchQty)'\
    ' VALUES(%d, %02d%02d, %d, %d, %d, %d, %d)'\
    % (req_type, match_hour, match_min, open_pri, high_pri, low_pri, close_pri, tol_match_qty - tol_match_qty_prev)
cursor.execute(sql)
conn.commit()
print('[%05d] %s' % (ii + 1, sql))

src_file.close()
conn.close()
