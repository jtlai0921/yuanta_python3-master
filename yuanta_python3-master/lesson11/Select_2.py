import sqlite3

conn = sqlite3.connect('demo.db')
cursor = conn.cursor() # 建立 cursor

# 查詢資料列 SQL
sql = 'SELECT id, n1, n2, n3, n4, n5, n6, ts FROM lotto'
cursor.execute(sql)
# 印出每列全部欄位(lo)/個別欄位(lo[n])的資料
lottos = [lo[2] for lo in cursor.fetchall()]
print(lottos)

conn.close()
