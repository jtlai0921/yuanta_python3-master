import sqlalchemy
from sqlalchemy import create_engine, DateTime, Column, Integer, String, func, text, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import tkinter

Base = declarative_base()

class DBAgent:
    def __init__(self):
        self.engine = create_engine("sqlite:///Homework20190708.db", echo=False)
        global Base
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def getSession(self):
        return self.session

    def close(self):
        self.session.close()

    def add(self, data):
        self.session.add(data)
        self.session.commit()

    def appendStockToFund(self, fund_id, stock_id):
        funds = self.session.query(Fund).filter(Fund.id == fund_id)
        stocks = self.session.query(Stock).filter(Stock.id == stock_id)
        if funds.count() == 1 and stocks.count() == 1:
            fund = funds[0]
            fund.stocks.append(stocks[0])
            self.session.commit()
            return fund
        raise Exception("找不到符合的條件")

    def removeStockFromFund(self, fund_id, stock_id):
        funds = self.session.query(Fund).filter(Fund.id == fund_id)
        stocks = self.session.query(Stock).filter(Stock.id == stock_id)
        if funds.count() == 1 and stocks.count() == 1:
            fund = funds[0]
            fund.stocks.remove(stocks[0])
            self.session.commit()
            return fund
        raise Exception("找不到符合的條件")

    def appendNavToFund(self, fund_id, nav):
        funds = self.session.query(Fund).filter(Fund.id == fund_id)
        if funds.count() == 1:
            fund = funds[0]
            fund.navs.append(nav)
            self.session.commit()
            return fund
        raise Exception("找不到符合的條件")

    def getStocks(self):
        return self.session.query(Stock)

    def getFunds(self):
        return self.session.query(Fund)

    def getManagers(self):
        return self.session.query(Manager)

    def getNavs(self):
        return self.session.query(Nav)


stock_funds = Table("stock_founds", Base.metadata,
                  Column('stock_id', ForeignKey("stock.id"), primary_key=True),
                  Column('fund_id', ForeignKey("fund.id"), primary_key=True))

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    funds = relationship("Fund", secondary=stock_funds, back_populates="stocks")

    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return "Stock('{}', '{}')".format(self.id, self.symbol)

class Fund(Base):
    __tablename__ = "fund"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stocks = relationship("Stock", secondary=stock_funds, back_populates="funds")
    # manager_id = Column(Integer, ForeignKey("manager.id"))
    manager = relationship("Manager", uselist=False, back_populates="fund")
    navs = relationship("Nav", uselist=True, back_populates="fund")

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Fund('{}', '{}', '{}', '{}', '{}')"\
            .format(self.id, self.name, [str(stock) for stock in self.stocks],
                    self.manager, [str(nav) for nav in self.navs])


class Manager(Base):
    __tablename__ = "manager"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fund_id = Column(Integer, ForeignKey("fund.id"))
    fund = relationship("Fund", uselist=False, back_populates="manager")

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Manager('{}', '{}', '{}')".format(self.id, self.name, self.fund_id)


class Nav(Base):
    __tablename__ = "nav"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.datetime.now())
    nav = Column(Integer)
    fund_id = Column(Integer, ForeignKey("fund.id"))
    fund = relationship("Fund", uselist=False, back_populates="navs")

    def __init__(self, nav, date=datetime.datetime.now()):
        self.nav = nav
        self.date = date

    def __str__(self):
        return "Nav('{}', '{}', '{}')".format(self.id, self.nav, self.date)


def closeBtn_Clicked(w, a):
    w.quit()
    a.close()


def button1_1Clicked(a, entry):
    print("## 新增股票(成份股) ##")
    stock_symbol = entry.get()
    if len(stock_symbol) == 0:
        return
    stocks = a.getStocks().filter(Stock.symbol == stock_symbol)
    if stocks.count() > 0:
        print("股票已存在" + stock_symbol)
        return
    stock = Stock(stock_symbol)
    a.add(stock)
    print(stock)


def button1_2Clicked(a):
    print("## 查詢股票(成份股) ##")
    for stock in a.getStocks():
        print(stock)


def button2_1Clicked(a, entry1, entry2):
    print("## 新增基金與經理人 ##")
    fund_name = entry1.get()
    manager_name = entry2.get()
    if len(fund_name) == 0 or len(manager_name) == 0:
        return
    fund = Fund(fund_name)
    fund.manager = Manager(manager_name)
    a.add(fund)
    print(fund)


def button2_2Clicked(a):
    print("## 查詢基金與經理人 ##")
    for fund in a.getFunds():
        print(fund)


def button3_1Clicked(a, entry1, entry2):
    print("## 基金-新增成分股 ##")
    try:
        fund_id = int(entry1.get())
        stock_id = int(entry2.get())
        print(a.appendStockToFund(fund_id, stock_id))
    except BaseException as e:
        print(e)
        return


def button3_2Clicked(a, entry1, entry2):
    print("## 基金-刪除成分股 ##")
    try:
        fund_id = int(entry1.get())
        stock_id = int(entry2.get())
        print(a.removeStockFromFund(fund_id, stock_id))
    except BaseException as e:
        print(e)
        return


def button4Clicked(a, entry1, entry2, entry3=None):
    print("## 基金-新增nav資料 ##")
    try:
        fund_id = int(entry1.get())
        nav_value = int(entry2.get())
        if entry3 is None:
            nav_date = datetime.datetime.now()
        else:
            nav_date = datetime(entry3.get())
        print(a.appendNavToFund(fund_id, Nav(nav_value, nav_date)))
    except BaseException as e:
        print(e)
        return

def button5Clicked(a, entry1):
    print("## 基金-查詢基金可一併查出成分股、經理人、nav list ##")
    try:
        fund_id = int(entry1.get())
        funds = a.getFunds().filter(Fund.id == fund_id)
        if funds.count() == 1:
            fund = funds[0]
            print(fund)
    except BaseException as e:
        print(e)
        return

def button6Clicked(a, entry1):
    print("## 基金-查詢股票可以查出有哪些基金有投資使用 ##")
    try:
        stock_id = int(entry1.get())
        stocks = a.getStocks().filter(Stock.id == stock_id)
        if stocks.count() == 1:
            stock = stocks[0]
            for fund in a.getFunds():
                if fund.stocks.count(stock) > 0:
                    print(fund)
    except BaseException as e:
        print(e)
        return


agent = DBAgent()

win = tkinter.Tk()
win.title("基金管理")
win.geometry("1000x300")

panel1 = tkinter.Frame(win)
panel1.pack(fill=tkinter.BOTH)
panel1.pack_propagate(False)

panel1.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
panel1.columnconfigure((0, 1, 2), weight=1)

label1 = tkinter.Label(panel1, text="新增股票(成份股)")
label1.grid(row=0, column=0, pady=(5, 0))

subpanel1_1 = tkinter.Frame(panel1)
subpanel1_1.grid(row=0, column=1, pady=(5, 0))

tkinter.Label(subpanel1_1, text="股票代碼").pack(side=tkinter.LEFT)

entry1 = tkinter.Entry(subpanel1_1, justify=tkinter.CENTER)
entry1.pack(side=tkinter.LEFT)
entry1.config(width=10)
entry1.insert(0, "2330")

subpanel1_2 = tkinter.Frame(panel1)
subpanel1_2.grid(row=0, column=2, pady=(5, 0))

tkinter.Button(subpanel1_2, text="新增", command=lambda a=agent, entry=entry1: button1_1Clicked(a, entry))\
    .pack(side=tkinter.LEFT)
tkinter.Button(subpanel1_2, text="查詢", command=lambda a=agent: button1_2Clicked(a))\
    .pack(side=tkinter.LEFT)


label2 = tkinter.Label(panel1, text="新增基金與經理人")
label2.grid(row=1, column=0, pady=(5, 0))

subpanel2_1 = tkinter.Frame(panel1)
subpanel2_1.grid(row=1, column=1, pady=(5, 0))

tkinter.Label(subpanel2_1, text="基金名稱").pack(side=tkinter.LEFT)
entry2_1 = tkinter.Entry(subpanel2_1, justify=tkinter.CENTER)
entry2_1.pack(side=tkinter.LEFT)
entry2_1.config(width=10)
entry2_1.insert(0, "元大基金")

tkinter.Label(subpanel2_1, text="經理人").pack(side=tkinter.LEFT, padx=(10, 0))
entry2_2 = tkinter.Entry(subpanel2_1, justify=tkinter.CENTER)
entry2_2.pack(side=tkinter.LEFT)
entry2_2.config(width=10)
entry2_2.insert(0, "林董")

subpanel2_2 = tkinter.Frame(panel1)
subpanel2_2.grid(row=1, column=2, pady=(5, 0))

button2_1 = tkinter.Button(subpanel2_2, text="新增",
                           command=lambda a=agent, e1=entry2_1, e2=entry2_2: button2_1Clicked(a, e1, e2))\
    .pack(side=tkinter.LEFT)
button2_2 = tkinter.Button(subpanel2_2, text="查詢", command=lambda a=agent: button2_2Clicked(a))\
    .pack(side=tkinter.LEFT)


label3 = tkinter.Label(panel1, text="基金-新增/刪除成分股")
label3.grid(row=2, column=0, pady=(5, 0))

subpanel3_2 = tkinter.Frame(panel1)
subpanel3_2.grid(row=2, column=1, pady=(5, 0))

tkinter.Label(subpanel3_2, text="基金索引值").pack(side=tkinter.LEFT)
entry3_1 = tkinter.Entry(subpanel3_2, justify=tkinter.CENTER)
entry3_1.pack(side=tkinter.LEFT)
entry3_1.config(width=10)
entry3_1.insert(0, "1")

tkinter.Label(subpanel3_2, text="成分股索引值").pack(side=tkinter.LEFT, padx=(10, 0))
entry3_2 = tkinter.Entry(subpanel3_2, justify=tkinter.CENTER)
entry3_2.pack(side=tkinter.LEFT)
entry3_2.config(width=10)
entry3_2.insert(0, "1")

subpanel3_3 = tkinter.Frame(panel1)
subpanel3_3.grid(row=2, column=2, pady=(5, 0))

button3_1 = tkinter.Button(subpanel3_3, text="新增",
                           command=lambda a=agent, e1=entry3_1, e2=entry3_2: button3_1Clicked(a, e1, e2))\
    .pack(side=tkinter.LEFT)
button3_2 = tkinter.Button(subpanel3_3, text="刪除",
                           command=lambda a=agent, e1=entry3_1, e2=entry3_2: button3_2Clicked(a, e1, e2))\
    .pack(side=tkinter.LEFT)


label4 = tkinter.Label(panel1, text="基金-新增nav資料")
label4.grid(row=3, column=0, pady=(5, 0))

subpanel4 = tkinter.Frame(panel1)
subpanel4.grid(row=3, column=1, pady=(5, 0))

tkinter.Label(subpanel4, text="基金索引值").pack(side=tkinter.LEFT)
entry4_1 = tkinter.Entry(subpanel4, justify=tkinter.CENTER)
entry4_1.pack(side=tkinter.LEFT)
entry4_1.config(width=10)
entry4_1.insert(0, "1")

tkinter.Label(subpanel4, text="NAV值").pack(side=tkinter.LEFT, padx=(10, 0))
entry4_2 = tkinter.Entry(subpanel4, justify=tkinter.CENTER)
entry4_2.pack(side=tkinter.LEFT)
entry4_2.config(width=10)
entry4_2.insert(0, "100")

button4 = tkinter.Button(panel1, text="新增", command=lambda a=agent, e1=entry4_1, e2=entry4_2: button4Clicked(a, e1, e2))
button4.grid(row=3, column=2, pady=(5, 0))


label5 = tkinter.Label(panel1, text="基金-查詢基金可一併查出成分股、經理人、nav list")
label5.grid(row=4, column=0, pady=(5, 0))

subpanel5 = tkinter.Frame(panel1)
subpanel5.grid(row=4, column=1, pady=(5, 0))

tkinter.Label(subpanel5, text="基金索引值").pack(side=tkinter.LEFT)
entry5 = tkinter.Entry(subpanel5, justify=tkinter.CENTER)
entry5.pack(side=tkinter.LEFT)
entry5.config(width=10)
entry5.insert(0, "1")

button5 = tkinter.Button(panel1, text="查詢", command=lambda a=agent, e1=entry5: button5Clicked(a, e1))
button5.grid(row=4, column=2, pady=(5, 0))


label6 = tkinter.Label(panel1, text="基金-查詢股票可以查出有哪些基金有投資使用")
label6.grid(row=5, column=0, pady=(5, 0))

subpanel6 = tkinter.Frame(panel1)
subpanel6.grid(row=5, column=1, pady=(5, 0))

tkinter.Label(subpanel6, text="股票索引值").pack(side=tkinter.LEFT)
entry6 = tkinter.Entry(subpanel6, justify=tkinter.CENTER)
entry6.pack(side=tkinter.LEFT)
entry6.config(width=10)
entry6.insert(0, "1")

button6 = tkinter.Button(panel1, text="查詢", command=lambda a=agent, e1=entry6: button6Clicked(a, e1))
button6.grid(row=5, column=2, pady=(5, 0))

closeBtn = tkinter.Button(win, text="離開", command=lambda w=win, a=agent: closeBtn_Clicked(w, a))
closeBtn.pack()

win.mainloop()
