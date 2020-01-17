import sqlite3

conn = sqlite3.connect('lab.db')
print(conn)
conn.close()
