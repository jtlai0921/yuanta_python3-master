import sqlite3

class dbAgent:
    __conn = None
    __cursor = None
    __createSql = 'create table if not exists TX (' \
        'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
        'ReqType INTEGER, ' \
        'MatchTime INTEGER, ' \
        'MatchPri FLOAT, ' \
        'OpenPri FLOAT, ' \
        'HighPri FLOAT, ' \
        'LowPri FLOAT, ' \
        'TolMatchQty INTEGER, ' \
        'ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'

    __dropSql = 'drop table if exists TX'

    __selectSql = 'select ReqType, MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty, id from TX ' \
            'where ReqType=%d and MatchTime=%d'

    __selectSql2 = 'select ReqType, MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty from TX '

    __insertSql = 'insert into TX(ReqType, MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty) VALUES ' \
        '(%d, %d, %f, %f, %f, %f, %d)'

    __insertSql2 = 'insert into TX(ReqType, MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty) VALUES ' \
        '(?, ?, ?, ?, ?, ?, ?)'

    __updateSql = 'update TX set MatchPri=%f, HighPri=%f, LowPri=%f, TolMatchQty=%d where id=%d'

    __tableInfoSql = 'PRAGMA TABLE_INFO(TX)'

    def __init__(self, dbName):
        self.__conn = sqlite3.connect(dbName)
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute(self.__dropSql)
        self.__cursor.execute(self.__createSql)
        self.__conn.commit()

    def selectRow(self, reqType, matchTime):
        self.__cursor.execute(self.__selectSql % (reqType, int(matchTime[0:4])))
        rows = self.__cursor.fetchall()
        if len(rows) > 0:
            return rows[0]
        else:
            return None

    def __selectAllRow(self):
        self.__cursor.execute(self.__selectSql2)
        return self.__cursor.fetchall()

    def insertRow(self, reqType, matchTime, matchPri, qty):
        self.__cursor.execute(self.__insertSql % (reqType, int(matchTime[0:4]), matchPri, matchPri,
                                                  matchPri, matchPri, qty))
        self.__conn.commit()

    def insertRows(self, datas):
        self.__cursor.executemany(self.__insertSql2, datas)
        self.__conn.commit()

    def updateRow(self, row, matchPri, highPri, lowPri, qty):
        self.__cursor.execute(self.__updateSql % (matchPri, highPri, lowPri, qty, row[7]))
        self.__conn.commit()

    def print(self):
        self.__cursor.execute(self.__tableInfoSql)
        for name in [t[1] for t in self.__cursor.fetchall() if t[1] != "id" and t[1] != "ts"]:
            print("%10s" % name, end='\t')
        print("\n--------------------------------------------------------------------------------")
        for row in self.__selectAllRow():
            print("%10d\t%-10d\t%10.2f\t%10.2f\t%10.2f\t%10.2f\t%10d" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))


def readFile(path):
    rows = []
    try:
        file = open(filePath, "r", encoding="utf-8")
        lines = file.readlines()
        firstLine = True
        for oneLine in lines:
            if firstLine:
                firstLine = False
                continue
            fields = oneLine.split(",")
            # print(fields)
            rows.append([v.strip() for v in fields])
    except BaseException as e:
        print(e)
    return rows


filePath = "ticks.txt"
dbName = "Homework20190705.db"

db = dbAgent(dbName)

lastMinTolMatchQty = 0
currentMinTolMatchQty = 0
for data in readFile(filePath):
    # 一筆資料
    reqType = int(data[0])
    matchTime = data[1]
    matchPri = float(data[2])
    tolMatchQty = int(data[6])
    # 尋找同一分鐘區間的資料
    row = db.selectRow(reqType, matchTime)
    if row == None:
        # 新的分鐘區間
        # if currentMinTolMatchQty == 0:
        #     currentMinTolMatchQty = tolMatchQty
        lastMinTolMatchQty = currentMinTolMatchQty
        db.insertRow(reqType, matchTime, matchPri, tolMatchQty - lastMinTolMatchQty)
    else:
        # 已存在的分鐘區間
        highPri = row[4]
        lowPri = row[5]
        if matchPri > highPri:
            highPri = matchPri
        if matchPri < lowPri:
            lowPri = matchPri
        db.updateRow(row, matchPri, highPri, lowPri, tolMatchQty - lastMinTolMatchQty)
    currentMinTolMatchQty = tolMatchQty

db.print()