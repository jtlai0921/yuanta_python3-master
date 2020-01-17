# -*- coding: UTF-8 -*-
# Author: 元大證券資訊部溫鳳祥
# Desc: 使用元大報價 API 取得分 K 資料並寫入 SQLite DB

import wx, wx.grid, time, sys
from ctypes import byref, POINTER, windll
from comtypes import IUnknown, GUID
from comtypes.client import GetModule,  GetBestInterface, GetEvents
user32 = windll.user32
atl = windll.atl
import sqlite3


# 計算分 K 資料
req_type = -1
match_hour = -1
match_min = -1
open_pri = -1
high_pri = -1
low_pri = -1
close_pri = -1
tol_match_qty = -1
tol_match_qty_prev = -1

# grid column definitions
COL_MATCH_TIME = 0
COL_SYMBOL = 1
COL_OPEN_PRICE = 2
COL_HIGH_PRICE = 3
COL_LOW_PRICE = 4
COL_CLOSE_PRICE = 5
COL_TOTAL_QTY = 6
COL_REQ_TYPE = 7


# ----------------------------------------------------------------------
def GetTimeStr():
    return time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))

# ----------------------------------------------------------------------
class YuantaQuoteEvents(object):
    def __init__(self, parent, frame):
        self.parent = parent
        self.frame = frame
    def OnMktStatusChange (self, this, Status, Msg, ReqType):
        print ('OnMktStatusChange {},{},{}'.format (ReqType, Msg, Status))
        self.frame.tcLoginStatus.Clear()
        self.frame.tcLoginStatus.WriteText('{} {} ReqType={}'.format(GetTimeStr(), Msg, ReqType))
    def OnRegError(self, this, symbol, updmode, ErrCode, ReqType):
        print ('OnRegError {},{},{},{}'.format (ReqType, ErrCode, symbol, updmode))
    def OnGetMktData(self, this, PriType, symbol, Qty, Pri, ReqType):
        print ('OnGetMktData')
    def OnGetMktQuote(self, this, symbol, DisClosure, Duration, ReqType):
        print ('OnGetMktQuote')
    def OnGetMktAll(self, this, symbol, RefPri, OpenPri, HighPri, LowPri, UpPri, DnPri, MatchTime, MatchPri, MatchQty, TolMatchQty,
        BestBuyQty, BestBuyPri, BestSellQty,BestSellPri, FDBPri, FDBQty, FDSPri, FDSQty, ReqType):
        global req_type, match_hour, match_min, open_pri, high_pri, low_pri, close_pri, tol_match_qty, tol_match_qty_prev
        # print('OnGetMktAll: {} {} c:{} o:{} h:{} l:{} v:{}'.format(ReqType, MatchTime, MatchPri, OpenPri, HighPri, LowPri, TolMatchQty))

        req_type_tmp = int(ReqType)
        match_hour_tmp = int(MatchTime[0:2])
        match_min_tmp = int(MatchTime[2:4])
        match_sec_tmp = int(MatchTime[4:6])
        match_ms_tmp = int(MatchTime[6:])
        open_pri_tmp = int(OpenPri)
        high_pri_tmp = int(HighPri)
        low_pri_tmp = int(LowPri)
        close_pri_tmp = int(MatchPri)
        tol_match_qty_tmp = int(TolMatchQty)
        print('OnGetMktAll: {:02d}:{:02d}:{:02d}.{:06d} [{}] o:{} h:{} l:{} c:{} v:{} r:{}'.format(
            match_hour_tmp, match_min_tmp, match_sec_tmp, match_ms_tmp,
            symbol, open_pri_tmp, high_pri_tmp, low_pri_tmp, close_pri_tmp,
            tol_match_qty_tmp,
            req_type_tmp))

        if self.frame.grid1.InsertRows(0, 1):
            row = 0
            _matchTime = '{:02d}:{:02d}:{:02d}.{:06d}'.format(match_hour_tmp, match_min_tmp, match_sec_tmp, match_ms_tmp)
            self.frame.grid1.SetCellValue(row, COL_MATCH_TIME, _matchTime)
            self.frame.grid1.SetCellValue(row, COL_SYMBOL, symbol)
            self.frame.grid1.SetCellValue(row, COL_OPEN_PRICE, str(open_pri_tmp))
            self.frame.grid1.SetCellValue(row, COL_HIGH_PRICE, str(high_pri_tmp))
            self.frame.grid1.SetCellValue(row, COL_LOW_PRICE, str(low_pri_tmp))
            self.frame.grid1.SetCellValue(row, COL_CLOSE_PRICE, str(close_pri_tmp))
            self.frame.grid1.SetCellValue(row, COL_TOTAL_QTY, str(tol_match_qty_tmp))
            self.frame.grid1.SetCellValue(row, COL_REQ_TYPE, str(req_type_tmp))

            # self.SetCellColor(self.frame.grid1, row, COL_OPEN_PRICE, RefPri, OpenPri)
            # self.SetCellColor(self.frame.grid1, row, COL_HIGH_PRICE, RefPri, HighPri)
            # self.SetCellColor(self.frame.grid1, row, COL_LOW_PRICE, RefPri, LowPri)
            # self.SetCellColor(self.frame.grid1, row, COL_MATCH_PRICE, RefPri, MatchPri)

        if req_type != req_type_tmp or match_hour != match_hour_tmp or match_min != match_min_tmp:
            if req_type > -1 and match_hour > -1 and match_min > -1:
                # print('OnGetMktAll: Write MinK: {:02d}:{:02d} [{}] o:{} h:{} l:{} c:{} v:{} r:{}'.format(
                #     match_hour, match_min, symbol, open_pri, high_pri, low_pri, close_pri, tol_match_qty - tol_match_qty_prev, req_type))
                frame.WriteMinK(match_hour, match_min, symbol, open_pri, high_pri, low_pri, close_pri, tol_match_qty - tol_match_qty_prev, req_type)
                tol_match_qty_prev = tol_match_qty
                tol_match_qty = tol_match_qty_tmp
            else:   # first data item
                tol_match_qty = tol_match_qty_tmp
                tol_match_qty_prev = 0

            req_type = req_type_tmp
            match_hour = match_hour_tmp
            match_min = match_min_tmp
            open_pri = close_pri_tmp
            high_pri = close_pri_tmp
            low_pri = close_pri_tmp
            close_pri = close_pri_tmp

        else:   # same req_type & match_hour & match_min
            if high_pri < close_pri_tmp:
                high_pri = close_pri_tmp
            if low_pri > close_pri_tmp:
                low_pri = close_pri_tmp
            close_pri = close_pri_tmp
            tol_match_qty = tol_match_qty_tmp


    def OnGetDelayClose(self, this, symbol, DelayClose, ReqType):
        print ('OnGetDelayClose')
    def OnGetBreakResume(self, this, symbol, BreakTime, ResumeTime, ReqType):
        print ('OnGetBreakResume')
    def OnGetTradeStatus(self, this, symbol, TradeStatus, ReqType):
        print ('OnGetTradeStatus')
    def OnTickRegError(self, this, strSymbol, lMode, lErrCode, ReqType):
        print ('OnTickRegError')
    def OnGetTickData(self, this, strSymbol, strTickSn, strMatchTime, strBuyPri, strSellPri, strMatchPri, strMatchQty, strTolMatQty,
        strMatchAmt, strTolMatAmt, ReqType):
        print ('OnGetTickData')
    def OnTickRangeDataError(self, this, strSymbol, lErrCode, ReqType):
        print ('OnTickRangeDataError')
    def OnGetTickRangeData(self, this, strSymbol, strStartTime, strEndTime, strTolMatQty, strTolMatAmt, ReqType):
        print ('OnGetTickRangeData')
    def OnGetTimePack(self, this, strTradeType, strTime, ReqType):
        print ('OnGetTimePack {},{}'.format (strTradeType, strTime))
    def OnGetDelayOpen(self, this, symbol, DelayOpen, ReqType):
        print ('OnGetDelayOpen')
    def OnGetFutStatus(self, this, symbol, FunctionCode, BreakTime, StartTime, ReopenTime, ReqType):
        print ('OnGetFutStatus')
    def OnGetLimitChange(self, this, symbol, FunctionCode, StatusTime, Level, ExpandType, ReqType):
        print ('OnGetLimitChange')

# ----------------------------------------------------------------------
class YuantaQuoteWrapper:
    def __init__(self, frame):#, bot):
        # self.bot = bot
        Iwindow = POINTER(IUnknown)()
        Icontrol = POINTER(IUnknown)()
        Ievent = POINTER(IUnknown)()
        res = atl.AtlAxCreateControlEx("YUANTAQUOTE.YuantaQuoteCtrl.1", frame.Handle, None,
                                    byref(Iwindow),
                                    byref(Icontrol),
                                    byref(GUID()),
                                    Ievent)
        self.YuantaQuote = GetBestInterface(Icontrol)
        self.YuantaQuoteEvents = YuantaQuoteEvents(self, frame)#, conn, cursor)
        self.YuantaQuoteEventsConnect = GetEvents(self.YuantaQuote, self.YuantaQuoteEvents)


# ----------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        # self.conn, self.cursor = CreateDb('ticks.db')
        self.CreateDb('ticks.db')
        self.Yuanta = None
        return True

    # create DB & table
    def CreateDb(self, fileName):
        self.conn = sqlite3.connect('ticks.db')
        self.cursor = self.conn.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS TK (' \
            'MatchTime INTEGER, '\
            'Symbol CHAR(25), '\
            'OpenPri INTEGER, '\
            'HighPri INTEGER, '\
            'LowPri INTEGER, '\
            'ClosePri INTEGER, '\
            'MatchQty INTEGER, '\
            'ReqType INTEGER)'
        self.cursor.execute(sql)
        # return conn, cursor

    def SetMktLogin(self, frame, host, port, offhour, id, pswd):
        self.frame = frame
        self.host = host
        self.port = port
        self.offhour = offhour
        self.id = id
        self.pswd = pswd

        self.Yuanta = YuantaQuoteWrapper(frame)
        self.Yuanta.YuantaQuote.SetMktLogon(self.id, self.pswd, self.host, self.port, self.offhour, 0)

    def AddMktReg(self, symbol, updMode, reqType):
        try:
            errCode = self.Yuanta.YuantaQuote.AddMktReg(symbol, updMode, reqType, 0)
            print("AddMktReg({}, {}, {}) = {}".format(symbol, updMode, reqType, errCode))
            self.frame.tcRegStatus.Clear()
            self.frame.tcRegStatus.WriteText('{}: {}'.format(GetTimeStr(), str(errCode)))
        except Exception as ex:
            print("AddMktReg() failed: %s" % str(ex))

    def DelMktReg(self, symbol, reqType):
        try:
            errCode = self.Yuanta.YuantaQuote.DelMktReg(symbol, reqType)
            print("DelMktReg({}, {}) = {}".format(symbol, reqType, errCode))
            self.frame.tcRegStatus.Clear()
            self.frame.tcRegStatus.WriteText('{}: {}'.format(GetTimeStr(), str(errCode)))
        except Exception as ex:
            print("DelMktReg() failed: %s" % str(ex))

    def Quit(self):
        print("Close DB connection")
        self.conn.close()

    def WriteMinK(self, match_hour, match_min, symbol, open_pri, high_pri, low_pri, close_pri, match_qty, req_type):
        sql = "INSERT INTO TK (MatchTime, Symbol, OpenPri, HighPri, LowPri, ClosePri, MatchQty, ReqType)"\
            " VALUES(%02d%02d, '%s', %d, %d, %d, %d, %d, %d)"\
            % (match_hour, match_min, symbol, open_pri, high_pri, low_pri, close_pri, match_qty, req_type)
        print('WriteMinK: %s' % sql)
        self.cursor.execute(sql)
        self.conn.commit()


# ----------------------------------------------------------------------
class MainFrame(wx.Frame):
    def __init__(self, parent, title, app, width=1000, height=700, host='10.214.8.64', port=80, id='', pswd='', symbol=''):
        super(MainFrame, self).__init__(parent, title=title, size=(width, height))
        self.app = app
        self.host = host
        self.port = port
        self.id = id
        self.pswd = pswd
        self.offhour = 1
        self.symbol = symbol

        self.InitUI()
        self.Centre()

    def InitUI(self):
        panel1 = wx.Panel(self)

        self.tcHost = wx.TextCtrl(panel1)
        self.tcPort = wx.TextCtrl(panel1, style=wx.TE_READONLY)
        self.tcId = wx.TextCtrl(panel1)
        self.tcPswd = wx.TextCtrl(panel1, style=wx.TE_PASSWORD)
        self.cbOffhour = wx.CheckBox(panel1, label='T+1')
        self.cbOffhour.Bind(wx.EVT_CHECKBOX, self.OnOffhour)
        self.btnLogin = wx.Button(panel1, label='Login')
        self.btnLogin.Bind(wx.EVT_BUTTON, self.OnLogin)
        self.tcLoginStatus = wx.TextCtrl(panel1, style=wx.TE_READONLY)
        # set default values
        self.tcHost.SetLabelText(self.host)
        self.tcPort.SetLabelText(str(self.port))
        self.tcId.SetLabelText(self.id)
        self.tcPswd.SetLabelText(self.pswd)

        self.tcSymbol = wx.TextCtrl(panel1)
        self.btnReg = wx.Button(panel1, label='Register')
        self.btnReg.Bind(wx.EVT_BUTTON, self.OnReg)
        self.btnUnreg = wx.Button(panel1, label='Unregister')
        self.btnUnreg.Bind(wx.EVT_BUTTON, self.OnUnreg)
        self.tcRegStatus = wx.TextCtrl(panel1, style=wx.TE_READONLY)
        self.btnQuit = wx.Button(panel1, label='Quit')
        self.btnQuit.Bind(wx.EVT_BUTTON, self.OnQuit)
        # set default values
        self.tcSymbol.SetLabelText(self.symbol)

        # info grid
        self.grid1 = wx.grid.Grid(panel1)
        self.grid1.CreateGrid(0, 8)
        self.grid1.SetColSize(0, 80)
        self.grid1.SetRowLabelSize(0)
        self.grid1.SetColLabelValue(0, '成交時間')
        self.grid1.SetColLabelValue(1, '商品代碼')
        self.grid1.SetColLabelValue(2, '開盤價')
        self.grid1.SetColLabelValue(3, '最高價')
        self.grid1.SetColLabelValue(4, '最低價')
        self.grid1.SetColLabelValue(5, '收盤價')
        self.grid1.SetColLabelValue(6, '總成交量')
        self.grid1.SetColLabelValue(7, '盤別')

        gs = wx.GridBagSizer(10, 10)
        gs.Add(wx.StaticText(panel1, label='Host:'), pos=(0, 0), span=(1, 1), flag=wx.EXPAND, border=5)
        gs.Add(wx.StaticText(panel1, label='Port:'), pos=(1, 0), span=(1, 1), flag=wx.EXPAND, border=5)
        gs.Add(wx.StaticText(panel1, label='ID:'), pos=(2, 0), span=(1, 1), flag=wx.EXPAND, border=5)
        gs.Add(wx.StaticText(panel1, label='Password:'), pos=(3, 0), span=(1, 1), flag=wx.EXPAND, border=5)
        gs.Add(self.cbOffhour, pos=(4, 0), span=(1, 1), flag=wx.EXPAND, border=5)

        gs.Add(self.tcHost, pos=(0, 1), span=(1, 4), flag=wx.EXPAND, border=5)
        gs.Add(self.tcPort, pos=(1, 1), span=(1, 1), flag=wx.EXPAND, border=5)
        gs.Add(self.tcId, pos=(2, 1), span=(1, 2), flag=wx.EXPAND, border=5)
        gs.Add(self.tcPswd, pos=(3, 1), span=(1, 2), flag=wx.EXPAND, border=5)
        gs.Add(self.btnLogin, pos=(5, 0), span=(1, 1), flag=wx.EXPAND, border=5)
        gs.Add(self.tcLoginStatus, pos=(5, 1), span=(1, 8), flag=wx.EXPAND, border=5)

        gs.Add(wx.StaticText(panel1, label='Symbol:'), pos=(0, 5), span=(1, 1), flag=wx.EXPAND, border=5)
        gs.Add(self.tcSymbol, pos=(0, 6), span=(1, 3), flag=wx.EXPAND, border=5)
        gs.Add(self.btnReg, pos=(1, 5), span=(1, 2), flag=wx.EXPAND, border=5)
        gs.Add(self.btnUnreg, pos=(1, 7), span=(1, 2), flag=wx.EXPAND, border=5)
        gs.Add(self.tcRegStatus, pos=(2, 5), span=(1, 4), flag=wx.EXPAND, border=5)

        gs.Add(self.grid1, pos=(6, 0), span=(10, 10), flag=wx.EXPAND, border=5)
        gs.Add(self.btnQuit, pos=(17, 9), span=(1, 1), flag=wx.EXPAND, border=5)

        panel1.SetSizer(gs)


    def OnOffhour(self, e):
        if self.cbOffhour.GetValue():
            self.offhour = 2
            self.tcPort.SetLabelText("82")
        else:
            self.offhour = 1
            self.tcPort.SetLabelText("80")

    def OnLogin(self, e):
        self.app.SetMktLogin(self, self.tcHost.GetLineText(0), self.tcPort.GetLineText(0), self.offhour, self.tcId.GetLineText(0), self.tcPswd.GetLineText(0))

    def OnReg(self, e):
        self.app.AddMktReg(self.tcSymbol.GetLineText(0), "4", self.offhour)

    def OnUnreg(self, e):
        self.app.DelMktReg(self.tcSymbol.GetLineText(0), self.offhour)

    def OnQuit(self, e):
        self.app.Quit()
        self.Close(True)

    def WriteMinK(self, match_hour, match_min, symbol, open_pri, high_pri, low_pri, close_pri, match_qty, req_type):
        app.WriteMinK(match_hour, match_min, symbol, open_pri, high_pri, low_pri, close_pri, match_qty, req_type)

# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = MyApp()
    frame = MainFrame(None, "EW Quote API + SQLite Demo", app, width=700, height=600, \
        # host="10.214.8.64", port=80, id="D121242093", pswd="1234", symbol="TXFH9")
        host="apiquote.yuantafutures.com.tw", port=80, id="D121242093", pswd="1234", symbol="TXFH9")
    frame.Show(True)
    app.MainLoop()
