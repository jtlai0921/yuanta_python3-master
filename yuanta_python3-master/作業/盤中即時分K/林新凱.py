import tkinter.ttk as ttk
import tkinter.messagebox
import os
import threading
import sqlite3

from ctypes import byref, POINTER, windll
from comtypes import IUnknown, GUID
from comtypes.client import GetModule, GetBestInterface, GetEvents
user32 = windll.user32
atl = windll.atl


class dbAgent:
    __conn = None
    __cursor = None

    __createSql = 'create table if not exists TX (' \
        'id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
        'ReqType INTEGER, ' \
        'MatchTime INTEGER, ' \
        'OpenPri FLOAT, ' \
        'HighPri FLOAT, ' \
        'LowPri FLOAT, ' \
        'MatchPri FLOAT, ' \
        'TolMatchQty INTEGER, ' \
        'ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'

    __dropSql = 'drop table if exists TX'

    __selectSql = 'select ReqType, MatchTime, OpenPri, HighPri, LowPri, MatchPri, TolMatchQty, id from TX ' \
            'where ReqType=%d and MatchTime=%d'

    __selectSql2 = 'select ReqType, MatchTime, OpenPri, HighPri, LowPri, MatchPri, TolMatchQty from TX '

    __insertSql = 'insert into TX(ReqType, MatchTime, OpenPri, HighPri, LowPri, MatchPri, TolMatchQty) VALUES ' \
        '(%d, %d, %f, %f, %f, %f, %d)'

    __insertSql2 = 'insert into TX(ReqType, MatchTime, OpenPri, HighPri, LowPri, MatchPri, TolMatchQty) VALUES ' \
        '(?, ?, ?, ?, ?, ?, ?)'

    __updateSql = 'update TX set HighPri=%f, LowPri=%f, MatchPri=%f, TolMatchQty=%d where id=%d'

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

    def updateRow(self, row, highPri, lowPri, matchPri, qty):
        self.__cursor.execute(self.__updateSql % (highPri, lowPri, matchPri, qty, row[7]))
        self.__conn.commit()

    def print(self):
        self.__cursor.execute(self.__tableInfoSql)
        for name in [t[1] for t in self.__cursor.fetchall() if t[1] != "id" and t[1] != "ts"]:
            print("%10s" % name, end='\t')
        print("\n--------------------------------------------------------------------------------")
        for row in self.__selectAllRow():
            print("%10d\t%-10d\t%10.2f\t%10.2f\t%10.2f\t%10.2f\t%10d" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))


dbName = "Homework20190715.db"
db = dbAgent(dbName)
lastMinTolMatchQty = 0
currentMinTolMatchQty = 0
yuantaApi = None

def regSymbol(strSymbol, ret_type):
    global yuantaApi
    ret = yuantaApi.YuantaQuote.AddMktReg(strSymbol, "4", ret_type, 0)
    print("AddMktReg {}".format(ret))


class YuantaQuoteEvents(object):
    def __init__(self, parent):
        self.parent = parent

    def OnMktStatusChange (self, this, Status, Msg, ReqType):
        print('OnMktStatusChange {},{},{}'.format (ReqType, Msg, Status))
        if Status == 2:
            threading.Thread(target=regSymbol, args=(entry3.get(), ReqType,)).start()

    def OnRegError(self, this, symbol, updmode, ErrCode, ReqType):
        print('OnRegError {},{},{},{}'.format (ReqType, ErrCode, symbol, updmode))
        tkinter.messagebox.showinfo("註冊失敗", symbol)

    def OnGetMktData(self, this, PriType, symbol, Qty, Pri, ReqType):
        print('OnGetMktData')

    def OnGetMktQuote(self, this, symbol, DisClosure, Duration, ReqType):
        print('OnGetMktQuote')

    def OnGetMktAll(self, this, symbol, RefPri, OpenPri, HighPri, LowPri, UpPri, DnPri, matchTime, MatchPri, MatchQty,
                    TolMatchQty, BestBuyQty, BestBuyPri, BestSellQty,BestSellPri, FDBPri, FDBQty, FDSPri, FDSQty,
                    reqType):
        #print ('OnGetMktAll\n')
        print('{} {} c:{} o:{} h:{} l:{} v:{}'.format(reqType, matchTime,  MatchPri, OpenPri, HighPri, LowPri,
                                                      TolMatchQty))
        # 尋找同一分鐘區間的資料
        matchPri = float(MatchPri)
        tolMatchQty = int(TolMatchQty)
        global currentMinTolMatchQty
        global lastMinTolMatchQty
        matchQty = tolMatchQty - lastMinTolMatchQty
        if matchQty > 0:
            row = db.selectRow(reqType, matchTime)
            if row == None:
                # 新的分鐘區間
                # if currentMinTolMatchQty == 0:
                #     currentMinTolMatchQty = tolMatchQty
                lastMinTolMatchQty = currentMinTolMatchQty
                db.insertRow(reqType, matchTime, matchPri, matchQty)

                row = db.selectRow(reqType, matchTime)
                if row is not None:
                    tree.insert("", "end", values=row)
            else:
                # 已存在的分鐘區間
                highPri = row[3]
                lowPri = row[4]
                if matchPri > highPri:
                    highPri = matchPri
                if matchPri < lowPri:
                    lowPri = matchPri
                db.updateRow(row, highPri, lowPri, matchPri, matchQty)

                row = db.selectRow(reqType, matchTime)
                tree.item(tree.get_children()[-1], values=row)
            currentMinTolMatchQty = tolMatchQty

    def OnGetDelayClose(self, this, symbol, DelayClose, ReqType):
        print('OnGetDelayClose')

    def OnGetBreakResume(self, this, symbol, BreakTime, ResumeTime, ReqType):
        print('OnGetBreakResume')

    def OnGetTradeStatus(self, this, symbol, TradeStatus, ReqType):
        print('OnGetTradeStatus')

    def OnTickRegError(self, this, strSymbol, lMode, lErrCode, ReqType):
        print('OnTickRegError')

    def OnGetTickData(self, this, strSymbol, strTickSn, strMatchTime, strBuyPri, strSellPri, strMatchPri, strMatchQty,
                      strTolMatQty, strMatchAmt, strTolMatAmt, ReqType):
        print('OnGetTickData')

    def OnTickRangeDataError(self, this, strSymbol, lErrCode, ReqType):
        print('OnTickRangeDataError')

    def OnGetTickRangeData(self, this, strSymbol, strStartTime, strEndTime, strTolMatQty, strTolMatAmt, ReqType):
        print('OnGetTickRangeData')

    def OnGetTimePack(self, this, strTradeType, strTime, ReqType):
        print('OnGetTimePack {},{}'.format (strTradeType, strTime))

    def OnGetDelayOpen(self, this, symbol, DelayOpen, ReqType):
        print('OnGetDelayOpen')

    def OnGetFutStatus(self, this, symbol, FunctionCode, BreakTime, StartTime, ReopenTime, ReqType):
        print('OnGetFutStatus')

    def OnGetLimitChange(self, this, symbol, FunctionCode, StatusTime, Level, ExpandType, ReqType):
        print('OnGetLimitChange')


class YuantaQuoteWapper:
    def __init__(self, handle):
        Iwindow = POINTER(IUnknown)()
        Icontrol = POINTER(IUnknown)()
        Ievent = POINTER(IUnknown)()
        res = atl.AtlAxCreateControlEx("YUANTAQUOTE.YuantaQuoteCtrl.1", handle, None,
                                       byref(Iwindow),
                                       byref(Icontrol),
                                       byref(GUID()),
                                       Ievent)
        self.YuantaQuote = GetBestInterface(Icontrol)
        self.YuantaQuoteEvents = YuantaQuoteEvents(self)
        self.YuantaQuoteEventsConnect = GetEvents(self.YuantaQuote, self.YuantaQuoteEvents)


def findBtnClicked():
    global yuantaApi
    print(entry1.get(), entry2.get())
    yuantaApi = YuantaQuoteWapper(win.winfo_id())
    yuantaApi.YuantaQuote.SetMktLogon(entry1.get(), entry2.get(), '203.66.93.84', '80', 1, 0)
    yuantaApi.YuantaQuote.SetMktLogon(entry1.get(), entry2.get(), '203.66.93.84', '82', 2, 1)


def closeBtnClicked():
    win.quit()


lastDataDate = None
dataLines = None
heading = {"1" : {"Name" : "盤別", "sortAsc" : True},
    "2" : {"Name" : "時間", "sortAsc" : True},
    "3" : {"Name" : "開盤價", "sortAsc" : True},
    "4" : {"Name" : "最高價", "sortAsc" : True},
    "5" : {"Name" : "最低價", "sortAsc" : True},
    "6" : {"Name" : "收盤價", "sortAsc" : True},
    "7" : {"Name" : "總量", "sortAsc" : True}}


win = tkinter.Tk()
win.title("即時k棒整理")
win.geometry("800x600")

panel1 = tkinter.Frame(win)
panel1.pack(fill=tkinter.BOTH)
panel1.pack_propagate(False)

panel1.rowconfigure((0, 1, 2, 3), weight=1)
panel1.columnconfigure((0, 1), weight=1)

label1 = tkinter.Label(panel1, text="登入帳號")
label1.grid(row=0, column=0, pady=(5, 0))

entry1 = tkinter.Entry(panel1, justify=tkinter.CENTER)
entry1.grid(row=0, column=1, pady=(5, 0))
entry1.insert(0, "YUANTA")

label2 = tkinter.Label(panel1, text="登入密碼")
label2.grid(row=1, column=0, pady=(5, 0))

entry2 = tkinter.Entry(panel1, justify=tkinter.CENTER, show="*")
entry2.grid(row=1, column=1, pady=(5, 0))
entry2.insert(0, "YUANTA")

label3 = tkinter.Label(panel1, text="報價代碼")
label3.grid(row=2, column=0, pady=(5, 0))

entry3 = tkinter.Entry(panel1, justify=tkinter.CENTER)
entry3.grid(row=2, column=1, pady=(5, 0))
entry3.insert(0, "TXFH9")

findBtn = tkinter.Button(panel1, text="連線", command=findBtnClicked)
findBtn.grid(row=3, column=0, pady=(5, 5))

closeBtn = tkinter.Button(panel1, text="關閉", command=closeBtnClicked)
closeBtn.grid(row=3, column=1, pady=(5, 5))

panel2 = tkinter.Frame(win, relief="sunken", borderwidth=3)
panel2.pack(fill=tkinter.BOTH, expand=True)
panel2.pack_propagate(False)

tree = ttk.Treeview(panel2, columns=tuple(key for key in heading.keys()), show="headings")
for key in heading.keys():
    tree.column(key, width=100, anchor="center")
    tree.heading(key, text=heading[key]["Name"])

tree.pack(fill=tkinter.BOTH, expand=True)
tree.pack_propagate(False)

win.mainloop()

