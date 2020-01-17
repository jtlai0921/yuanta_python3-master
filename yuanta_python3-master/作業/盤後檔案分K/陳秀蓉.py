import sqlite3
import os
import time
import datetime

def connect(sqlite_file):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    return conn, cursor

def close(conn):
    conn.close()

def CreatTable(conn, cursor):

    sql = 'create table if not exists ticks (' \
          'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
          'MatchTime   CHAR, ' \
          'MatchPri    INTEGER, ' \
          'OpenPri     INTEGER, ' \
          'HighPri     INTEGER, ' \
          'LowPri      INTEGER, ' \
          'TolMatchQty INTEGER, ' \
          'ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'

    cursor.execute(sql)  # 建立 ticks 資料表
    conn.commit()  # 執行資料庫更新

def print_header(cursor):
    print('\n ==> 取得分K資料結果')
    print('-----------------------------------------------')
    # 查詢 Table META-INFO
    cursor.execute('PRAGMA TABLE_INFO({})'.format('ticks'))
    names = [tup[1] for tup in cursor.fetchall()]
    for i, name in enumerate(names):
        if (i > 0):
            print(name, end='\t')
    print('\n-----------------------------------------------')

def delsel(type, conn, cursor):

    if (type == "D"): # 刪除程序
        sql = 'DELETE FROM ticks '
        cursor.execute(sql)  # 執行 SQL 語句
        conn.commit()
    else:
        sql = 'SELECT MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty, ts FROM ticks ORDER BY id '
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print('{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

def DealTq(conn, cursor):
    if (len(kd) > 0):
        bemt = kd[1][:4]
        sql = 'SELECT id, MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty FROM ticks WHERE MatchTime = %s ' % bemt
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is not None:  # 更新成交量
            # print('修改前：{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
            sql = 'Update ticks SET TolMatchQty=?, ts=? WHERE id=?'
            now = datetime.datetime.now()
            r6 = row[6]
            r6 = float(kd[6]) - r6
            cursor.execute(sql, (r6, now, row[0]))  # 執行 SQL 語句
            conn.commit()

def DealData(args, conn, cursor):
    if len(args[0].lstrip()) > 1:
        return
    mtd = args[1].lstrip()[:4]
    sql = 'SELECT id, MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty FROM ticks WHERE MatchTime = %s ' % mtd
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is not None:  # if row == not None update
        r4 = row[4]
        r5 = row[5]
        if r4 < float(args[4]):
            r4 = float(args[4])
        if r5 > float(args[5]):
            r5 = float(args[5])
        sql = 'Update ticks SET MatchPri=?, OpenPri=?, HighPri=?, LowPri=?, ts=? WHERE id=?'
        now = datetime.datetime.now()
        # print('修改前：{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        cursor.execute(sql, (row[2], row[3], r4, r5, now, row[0]))  # 執行 SQL 語句
    else:
        DealTq(conn, cursor)
        sql = 'INSERT INTO ticks(MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty) VALUES(?, ?, ?, ?, ?, ?)'
        cursor.execute(sql, (mtd, float(args[2].lstrip()), float(args[3].lstrip()), float(args[4].lstrip()), float(args[5].lstrip()), float(args[6].lstrip())))
    conn.commit()

    #清除前一筆放目前這筆資料
    kd.clear()
    for d in args:
        kd.append(d.lstrip())


kd = []  #存放前一筆資料
fpath = os.path.abspath('.')
conn, cursor = connect("demo.db")
CreatTable(conn, cursor)
delsel("D", conn, cursor)
with open('ticks.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        # time.sleep(0.0001)
        print(line.strip())  # 把末尾的'\n'刪掉
        DealData(line.strip().split(','), conn, cursor)

DealTq(conn, cursor) #處理最後一筆量
print_header(cursor) #讀取DB最後結果資料並印出來
delsel("S", conn, cursor)
close(conn)