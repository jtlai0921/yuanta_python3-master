import wx, time
import  wx.lib.anchors as anchors
from ctypes import byref, POINTER, windll
from comtypes import IUnknown, GUID
from comtypes.client import GetModule,  GetBestInterface, GetEvents
import queue as queue
import sqlite3
import datetime
user32 = windll.user32
atl = windll.atl


q = queue.Queue()
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False
    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
        
class Job:
    STOCK_LOGIN = 1
    STOCK_WATCH = 2
    def __init__(self, do_type, do_value = 0):
        self.do_type = do_type
        self.do_value = do_value
        q.put(self)
        
def DoJob(Bot, x):    
    for case in switch(x.do_type):
        if case(Job.STOCK_LOGIN):
            Bot.login()
            break
        if case(Job.STOCK_WATCH):
            Bot.watch(x.do_value)
            break
        
class YuantaQuoteEvents(object):
    def __init__(self, parent):
        self.parent = parent
    def OnMktStatusChange(self, this, Status, Msg, ReqType):
        print('OnMktStatusChange {},{},{}'.format (ReqType, Msg, Status))
        if Status == 2:
            Job(Job.STOCK_WATCH, ReqType)
    def OnRegError(self, this, symbol, updmode, ErrCode, ReqType):
        print('OnRegError {},{},{},{}'.format (ReqType, ErrCode, symbol, updmode))
    def OnGetMktData(self, this, PriType, symbol, Qty, Pri, ReqType):
        print('OnGetMktData')
    def OnGetMktQuote(self, this, symbol, DisClosure, Duration, ReqType):
        print('OnGetMktQuote')
    def OnGetMktAll(self, this, symbol, RefPri, OpenPri, HighPri, LowPri, UpPri, DnPri, MatchTime, MatchPri, MatchQty, TolMatchQty,
        BestBuyQty, BestBuyPri, BestSellQty,BestSellPri, FDBPri, FDBQty, FDSPri, FDSQty, ReqType):
        #print ('OnGetMktAll\n')
        dstr = '{},{},{},{},{},{},{}'.format(ReqType, MatchTime,  MatchPri, OpenPri, HighPri, LowPri, TolMatchQty)
        DealData(dstr, conn, cursor)
        print('{} {} c:{} o:{} h:{} l:{} v:{}'.format (ReqType, MatchTime,  MatchPri, OpenPri, HighPri, LowPri, TolMatchQty))
    def OnGetDelayClose(self, this, symbol, DelayClose, ReqType):
        print('OnGetDelayClose')
    def OnGetBreakResume(self, this, symbol, BreakTime, ResumeTime, ReqType):
        print('OnGetBreakResume')
    def OnGetTradeStatus(self, this, symbol, TradeStatus, ReqType):
        print('OnGetTradeStatus')
    def OnTickRegError(self, this, strSymbol, lMode, lErrCode, ReqType):
        print('OnTickRegError')
    def OnGetTickData(self, this, strSymbol, strTickSn, strMatchTime, strBuyPri, strSellPri, strMatchPri, strMatchQty, strTolMatQty,
        strMatchAmt, strTolMatAmt, ReqType):
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
    def __init__(self, handle, bot):
        self.bot = bot
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
        
class StockBot:
    def __init__(self, botuid, account, pwd):
        self.Yuanta = YuantaQuoteWapper (botuid, self)
        self.Account = account
        self.Pwd = pwd
    def login(self):
        #T port 80/443 , T+1 port 82/442 ,  reqType=1 T盤 , reqType=2  T+1盤 
        self.Yuanta.YuantaQuote.SetMktLogon(self.Account, self.Pwd, '10.214.8.64', '80', 1, 0)
        self.Yuanta.YuantaQuote.SetMktLogon(self.Account, self.Pwd, '10.214.8.64', '442', 2, 1)
        print('login')
    def watch(self, ret_type):
        ret = self.Yuanta.YuantaQuote.AddMktReg ('TXFH9', "4", ret_type, 0)
        print("AddMktReg {}".format(ret))
        print(type(ret))
        # DealData(line.strip().split(' '), conn, cursor)
        # for i in ret:
        #     print(str(i))
        
class MyApp(wx.App):
    def MainLoop(self, run_func):
        
        evtloop = wx.GUIEventLoop()
        old = wx.EventLoop.GetActive()
        wx.EventLoop.SetActive(evtloop)
        
        while self.keepGoing:
           
            run_func()
            while not q.empty():
                next_job = q.get()
                DoJob (Bot, next_job)
            
            while evtloop.Pending():
                evtloop.Dispatch()
           
            time.sleep(0.10)
            evtloop.ProcessIdle()
        wx.EventLoop.SetActive(old)
    def OnInit(self):
        self.keepGoing = True
        return True
    
def run_job():
    while not q.empty():
        next_job = q.get()
        DoJob(Bot, next_job)

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

def DealData(arg, conn, cursor):
    args = arg.split(',')
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


if __name__ == "__main__":
    kd = []  # 存放前一筆資料
    conn, cursor = connect("demo.db")
    CreatTable(conn, cursor)
    delsel("D", conn, cursor)
    app=MyApp()
    frame = wx.Frame(None,wx.ID_ANY,"Hello")
    frame.Show(False)
    Bot = StockBot(frame.Handle,'D121242093','1234')
    Job(Job.STOCK_LOGIN)
    app.MainLoop(run_job)

    #以下這段想寫在程序結束時,但暫時找不到python程序結束寫法
    DealTq(conn, cursor)  # 處理最後一筆量
    print_header(cursor)  # 讀取DB最後結果資料並印出來
    delsel("S", conn, cursor)
    close(conn)