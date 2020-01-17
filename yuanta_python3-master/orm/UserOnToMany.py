# -*- coding: utf-8 -*-
import datetime
import hashlib
from sqlalchemy import create_engine, DateTime, Column, Integer, String, func, text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

# 用來映對 Python 類別與資料庫表格之間的關聯
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.now())

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "User('{}','{}', '{}')".format(
            self.id,
            self.name,
            self.created_date
        )

class Address(Base):
    __tablename__ = 'user_address'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    '''代表若要從 User 關聯回 Address 就得存取 User 的 address 屬性'''
    user = relationship('User', backref=backref('address')) # 將 User 與 Address 之間以 address 屬性關聯起來

    def __init__(self, address):
        self.address = address
    def __str__(self):
        return "Address('{}')".format(self.address)

if __name__ == '__main__':
    ''' 1.建立 engine '''
    engine = create_engine('sqlite:///demo.db', echo=False)
    ''' 2.在資料庫內建立起相對應的表格 '''
    Base.metadata.create_all(engine)
    ''' 3.將 engine綁定(bind)到 Session 類別中'''
    Session = sessionmaker(bind=engine)
    ''' 4.將這個已經與 engine 綁定的 Session 類別實例化，以開始進行與資料庫的互動'''
    session = Session()

    # user_1 = User('user1')
    # user_2 = User('user2')
    # user_1.address = [Address('臺灣凱達格蘭大道')]
    # user_2.address = [Address('美國紐約時代廣場'), Address('美國華盛頓DC')]
    # session.add(user_1)
    # session.add(user_2)
    for r in session.query(Address):
        print(r.id, r.address, r.user_id)

    for r in session.query(User):
        for a in r.address:
            print(r.name, 'living at', a.address)

    # 提交到資料庫中儲存:
    session.commit()

    # 關閉 session:
    session.close()