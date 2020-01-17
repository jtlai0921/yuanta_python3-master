import sqlite3

conn = sqlite3.connect('demo.db')
cursor = conn.cursor() # 建立 cursor

# 查詢 Table META-INFO
cursor.execute('PRAGMA TABLE_INFO({})'.format('lotto'))
names = [t[1] for t in cursor.fetchall()]
for name in names:
    print(name, end='\t')
print('\n-----------------------------------------------')

# 查詢資料列 SQL
sql = 'SELECT id, n1, n2, n3, n4, n5, n6, ts FROM lotto'
cursor.execute(sql)
rows = cursor.fetchall()
for row in rows:
    print('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

conn.close()