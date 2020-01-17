import sqlite3

conn = sqlite3.connect('demo.db')
cursor = conn.cursor() # 建立 cursor
cursor.execute('INSERT INTO lotto(n1, n2, n3, n4, n5, n6) '
               'VALUES (%d,%d,%d,%d,%d,%d)' % (1, 2, 3, 4, 5, 6))

print(cursor.lastrowid) # 取得最新一筆 id

conn.commit() # 執行資料庫更新

conn.close()

print('新增成功')