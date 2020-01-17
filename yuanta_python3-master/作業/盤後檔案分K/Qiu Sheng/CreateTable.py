import sqlite3

sql = 'create table if not exists TX (' \
      'ReqType VARCHAR , ' \
      'MatchTime VARCHAR PRIMARY KEY, ' \
      'MatchPri VARCHAR, ' \
      'OpenPri VARCHAR, ' \
      'HighPri VARCHAR, ' \
      'LowPri VARCHAR, ' \
      'TolMatchQty INTEGER)'

conn = sqlite3.connect('homework.db')
cursor = conn.cursor()  # 建立 cursor
cursor.execute(sql)  # 建立 lotto 資料表

conn.commit()  # 執行資料庫更新
conn.close()
print('建立成功')