# -*- coding: UTF-8 -*-
# Author: 元大證券資訊部溫鳳祥
# Desc:  以 SQLAlchemy ORM 實作基金與成分股的 CRUD 操作

import sys
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, DateTime, Column, Integer, String, func, text, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship

# 1.用來映對 Python 類別與資料庫表格之間的關聯
Base = declarative_base()

# 'Many to many' relationships between stock & fund
refFundStock = Table('ref_fund_stock', Base.metadata,
    Column('fund_id', Integer, ForeignKey('fund.id')),
    Column('stock_id', Integer, ForeignKey('stock.id')))


# 個股
class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    # 'Many to many' relationship with Fund
    funds = relationship('Fund', secondary=refFundStock, back_populates='stocks')

    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return "<Stock: id={}, symbol='{}'>".format(self.id, self.symbol)


# 基金
class Fund(Base):
    __tablename__ = 'fund'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # 'Many to many' relationship with Stock
    stocks = relationship('Stock', secondary=refFundStock, back_populates='funds')
    # 'One to One' relationship with Manager
    manager = relationship('Manager', back_populates='fund', uselist=False)
    # 'One to Many' relationship with Nav
    nav = relationship('Nav', back_populates='fund', uselist=True)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<Fund: id={}, name='{}'>".format(self.id, self.name)


# 基金經理人
class Manager(Base):
    __tablename__ = 'manager'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # 'One to One' relationship with Fund
    fund_id = Column(Integer, ForeignKey('fund.id'))
    fund = relationship('Fund', back_populates='manager', uselist=False)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "<Manager: id={}, name='{}' fund_id={}>".format(self.id, self.name, self.fund_id)


# 基金淨值
class Nav(Base):
    __tablename__ = 'nav'
    id = Column(Integer, primary_key=True)
    # date = Column(DateTime, default=datetime.datetime.now())
    date = Column(String)
    nav = Column(Integer)
    # 'One to Many' relationship with Fund
    fund_id = Column(Integer, ForeignKey('fund.id'))
    fund = relationship('Fund', back_populates='nav', uselist=True)

    def __init__(self, date, nav):
        self.date = date
        self.nav = nav

    def __str__(self):
        return "<Nav: id={}, date={}, nav={}, fund_id={}>".format(self.id, self.date, self.nav, self.fund_id)


def getSession():
    # 2.建立 engine
    engine = create_engine('sqlite:///orm_lab.db', echo=False)
    # 3.在資料庫內建立起相對應的表格
    Base.metadata.create_all(engine)
    # 4.將 engine綁定(bind)到 Session 類別中
    Session = sessionmaker(bind=engine)
    # 5.將這個已經與 engine 綁定的 Session 類別實例化，以開始進行與資料庫的互動
    session = Session()
    return engine, session


# 新增股票
def addStock(isStockExistOk=False):
    symbol = input("請輸入股票代碼：")
    stock = session.query(Stock).filter_by(symbol=symbol).first()
    if stock:   # stock already exists
        if isStockExistOk:
            print("### 股票 '{}' 已存在: {}".format(symbol, stock))
            return 1, stock
        else:
            print("股票 '{}' 的資料已經存在，請勿重覆新增！".format(symbol))
            input("請按 Enter 繼續...")
            return -1, None

    # create a new stock
    stock = Stock(symbol)
    session.add(stock)
    session.commit()
    print("股票 '{}' 已經新增完成: {}".format(stock.symbol, stock))
    if not isStockExistOk:
        input("請按 Enter 繼續...")
    return 0, stock


# 新增基金與經理人
def addFundAndManager(isFundExistOk=False):
    fundName = input("請輸入基金名稱：")
    fund = session.query(Fund).filter_by(name=fundName).first()
    if fund:     # fund already exists
        if isFundExistOk:
            print("### 基金 '{}' 已存在: {}".format(fundName, fund))
            return 1, fund
        else:
            print("基金 '{}' 的資料已經存在，請勿重覆新增！".format(fundName))
            input("請按 Enter 繼續...")
            return -1, None
    else:   # create a new fund
        fund = Fund(fundName)

    mgrName = input("請輸入經理人姓名：")
    manager = session.query(Manager.id).filter_by(name=mgrName).first()
    if manager:
        print("*ERR* 經理人 '{}' 的資料已經存在，請勿重覆新增！".format(mgrName))
        input("請按 Enter 繼續...")
        return -1, None

    manager = Manager(mgrName)
    fund.manager = manager
    manager.fund = fund

    session.add(fund)
    session.add(manager)
    session.commit()
    print("基金 '{}' 和經理人 '{}' 已新增完成: {}, {}".format(fund.name, manager.name, fund, manager))
    if not isFundExistOk:
        input("請按 Enter 繼續...")
    return 0, fund


# 基金增加成分股
def fundAddStock():
    ret, fund = addFundAndManager(isFundExistOk=True)
    if ret < 0:
        return

    ret, stock = addStock(isStockExistOk=True)
    if ret < 0:
        return

    if stock in fund.stocks:
        print("*ERR* 基金 '{}' 已有成分股 '{}'，請勿重覆新增！".format(fund.name, stock.symbol))
        input("請按 Enter 繼續...")
        return

    fund.stocks.append(stock)
    stock.funds.append(fund)
    session.commit()
    print("成分股 '{}' 已加入基金 '{}'".format(stock.symbol, fund.name))
    input("請按 Enter 繼續...")


# 刪除基金的成分股
def fundDelStock():
    fundName = input("請輸入基金名稱：")
    rows = session.query(Fund).filter_by(name=fundName)
    if rows.count() == 0:
        print("*ERR* 基金 '{}' 不存在！".format(fundName))
        input("請按 Enter 繼續...")
        return
    elif rows.count() > 1:
        print("*ERR* 基金 '{}' 在 DB 中有重覆的資料，作業中止。".format(fundName))
        input("請按 Enter 繼續...")
        return
    fund = rows.first()

    symbol = input("請輸入股票代碼：")
    print()
    rows = session.query(Stock).filter_by(symbol=symbol)
    if rows.count() == 0:
        print("*ERR* 股票 '{}' 不存在！".format(symbol))
        input("請按 Enter 繼續...")
        return
    elif rows.count() > 1:
        print("*ERR* 股票 '{}' 在 DB 中有重覆的資料，作業中止。".format(symbol))
        input("請按 Enter 繼續...")
        return
    stock = rows.first()

    if stock not in fund.stocks and fund not in stock.funds:
        print("*ERR* 基金 '{}' 不含成分股 '{}'，無法刪除！".format(fundName, symbol))
        input("請按 Enter 繼續...")
        return
    if stock in fund.stocks:
        fund.stocks.remove(stock)
        print("### 刪除與基金 '{}' 相關聯的股票 '{}'".format(fund, stock))
    if fund in stock.funds:
        stock.funds.remove(fund)
        print("### 刪除與股票 '{}' 相關聯的基金 '{}'".format(stock, fund))
    session.commit()
    print("已從基金 '{}' 刪除成分股 '{}'".format(fund.name, stock.symbol))
    input("請按 Enter 繼續...")


# 新增基金淨值
def fundAddNav():
    foundFund = False

    ret, fund = addFundAndManager(isFundExistOk=True)
    if ret < 0:
        return
    elif ret > 0:
        foundFund = True

    date = input("請輸入基金淨值的日期(YYYY/MM/DD)：")
    if len(date) < 10 \
        or not date[:4].isnumeric() \
        or not date[5:7].isnumeric() \
        or not date[8:].isnumeric() \
        or date[4] != '/' \
        or date[7] != '/':
        print("*ERR* 日期格式錯誤！")
        input("請按 Enter 繼續...")
        return
    if foundFund:   # check if nav already exists
        rows = session.query(Nav).filter_by(fund_id=fund.id, date=date)
        if rows.count() == 1:
            nav = rows.first()
            # print("*ERR* 基金 '{}' 已有淨值({})的資料，請勿重覆新增！".format(fund.name, nav))
            print("*ERR* 基金 '{}' 已有淨值(date={}, nav={})的資料，請勿重覆新增！".format(fund.name, nav.date, nav.nav))
            input("請按 Enter 繼續...")
            return
        elif rows.count() > 1:
            print("*ERR* 淨值 '{}' 在 DB 中有重覆的資料，作業中止。".format(nav))
            input("請按 Enter 繼續...")
            return

    val = input("請輸入基金淨值的數值：")
    nav = Nav(date, val)
    nav.fund_id = fund.id
    session.add(nav)
    session.commit()
    # print("基金 '{}' 已新增淨值資料({})".format(fund.name, nav))
    print("基金 '{}' 已新增淨值資料(date={}, nav={})".format(fund.name, nav.date, nav.nav))
    input("請按 Enter 繼續...")


# 查詢基金與其經理人、成分股、淨值
def queryFund():
    fundName = input("請輸入基金名稱(ALL=顯示全部)：")
    print()
    if fundName.upper() == 'ALL':
        rows = session.query(Fund)
        if rows.count() == 0:
            print("沒有任何基金資料！")
            input("請按 Enter 繼續...")
            return
    else:
        rows = session.query(Fund).filter_by(name=fundName)
        if rows.count() == 0:
            print("*ERR* 基金 '{}' 不存在！".format(fundName))
            input("請按 Enter 繼續...")
            return
        elif rows.count() > 1:
            print("*ERR* 基金 '{}' 在 DB 中有重覆的資料，作業中止".format(fundName))
            input("請按 Enter 繼續...")
            return

    for fund in rows:
        print("基金：{}".format(fund.name))
        # print("基金：{}".format(fund))

        rows = session.query(Manager).filter_by(fund_id=fund.id)
        if rows.count() == 0:
            print("\t經理人：無")
        else:
            manager = rows.first()
            print("\t經理人：{}".format(manager.name))
            # print("\t經理人：{}".format(manager))

        if len(fund.stocks) == 0:
            print("\t成分股：無")
        else:
            for stk in fund.stocks:
                print("\t成分股：{}".format(stk.symbol))
                # print("\t成分股：{}".format(stk))

        rows = session.query(Nav).filter_by(fund_id=fund.id)
        if rows.count() == 0:
            print("\t淨值：無")
        else:
            for nav in rows:
                print("\t淨值：date={}, nav={}".format(nav.date, nav.nav))
                # print("\t淨值：{}".format(nav))
        # print()
    input("請按 Enter 繼續...")


# 查詢股票與相關的基金
def queryStock():
    symbol = input("請輸入股票名稱(ALL=顯示全部)：")
    print()
    if symbol.upper() == 'ALL':
        rows = session.query(Stock)
        if rows.count() == 0:
            print("沒有任何股票資料！")
            input("請按 Enter 繼續...")
            return
    else:
        rows = session.query(Stock).filter_by(symbol=symbol)
        if rows.count() == 0:
            print("*ERR* 股票 '{}' 不存在！".format(symbol))
            input("請按 Enter 繼續...")
            return
        elif rows.count() > 1:
            print("*ERR* 股票 '{}' 在 DB 中有重覆的資料，作業中止".format(symbol))
            input("請按 Enter 繼續...")
            return

    for stock in rows:
        print("股票：{}".format(stock.symbol))
        # print("股票：{}".format(stock))

        if len(stock.funds) == 0:
            print("\t基金：無")
        else:
            for fund in stock.funds:
                print("\t基金：{}".format(fund.name))
                # print("\t基金：{}".format(fund))
        # print()
    input("請按 Enter 繼續...")


if __name__ == '__main__':
    engine, session = getSession()
    if len(sys.argv) >= 2:
        engine.echo = (sys.argv[1] == '1' or sys.argv[1].upper() == 'T')

    while True:
        print('\n' + '=' * 80)
        print('1. 新增股票(成分股)')
        print('2. 新增基金與經理人')
        print('3. 基金 - 新增成分股')
        print('4. 基金 - 刪除成分股')
        print('5. 基金 - 新增 nav(淨值)資料')
        print('6. 查詢 - 查詢基金(可一併查出成分股、經理人、nav list)')
        print('7. 查詢 - 查詢股票(可以查出有哪些基金有投資使用)')
        print('Q. Quit')
        print()
        ans = input('請輸入選項：')

        # try:
        if ans == '1':
            addStock()
        elif ans == '2':
            addFundAndManager()
        elif ans == '3':
            fundAddStock()
        elif ans == '4':
            fundDelStock()
        elif ans == '5':
            fundAddNav()
        elif ans == '6':
            queryFund()
        elif ans == '7':
            queryStock()
        if ans.upper() == 'Q':
            break
        # except Exception as e:
        #     print("{}: {}".format(type(e), str(e)))
        # except Error as e:
        #     print("{}: {}".format(type(e), str(e)))

    session.close()
    print('Bye!')
