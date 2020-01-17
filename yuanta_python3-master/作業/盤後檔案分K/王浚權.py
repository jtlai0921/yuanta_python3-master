import pandas as pd
import sqlite3

df = pd.read_csv('ticks.txt', skipinitialspace=True)

sql = 'create table if not exists TX (' \
      'ReqType INTEGER, ' \
      'MatchTime INTEGER, ' \
      'MatchPri INTEGER, ' \
      'OpenPri INTEGER, ' \
      'HighPri INTEGER, ' \
      'LowPri INTEGER, ' \
      'TolMatchQty INTEGER)'

conn = sqlite3.connect('MinK.db')
cursor = conn.cursor()  # 建立 cursor
cursor.execute(sql)  # 建立 lotto 資料表

begtime = df.iloc[0, :]['MatchTime']
endtime = df.iloc[-1, :]['MatchTime']
sectime = int(begtime / 100000000 + 1) * 100000000
while sectime < endtime:
    df2 = df[(df['MatchTime'] >= begtime) & (df['MatchTime'] < sectime)]

    ReqType = df2.iloc[0, :]['ReqType']  # ReqType
    MatchTime = sectime  # MatchTime
    MatchPri = df2.iloc[-1, :]['MatchPri']  # MatchPri
    OpenPri = df2.iloc[0, :]['MatchPri']  # OpenPri
    HighPri = df2['MatchPri'].max()  # HighPri
    LowPri = df2['MatchPri'].min()  # LowPri
    TolMatchQty = df2.iloc[-1, :]['TolMatchQty'] - df2.iloc[0, :]['TolMatchQty']  # TolMatchQty

    cursor.execute('INSERT INTO TX(ReqType, MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty) ' \
                   'VALUES (%d,%d,%d,%d,%d,%d,%d)' % (
                   ReqType, MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty))

    conn.commit()  # 執行資料庫更新

    begtime = sectime
    sectime = int(sectime / 100000000 + 1) * 100000000

# 查詢資料列 SQL
sql = 'SELECT * FROM TX'
cursor.execute(sql)
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.commit()  # 執行資料庫更新
conn.close()