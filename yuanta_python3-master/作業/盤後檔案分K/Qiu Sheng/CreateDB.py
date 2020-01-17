import sqlite3

conn = sqlite3.connect('homework.db')
print(conn)
conn.close()