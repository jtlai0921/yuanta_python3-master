# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import create_engine, DateTime, Column, Integer, String, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

''' 1.用來映對 Python 類別與資料庫表格之間的關聯 '''
Base = declarative_base()
''' 2.建立 engine '''
engine = create_engine('sqlite:///demo.db', echo=False)
''' 3.在資料庫內建立起相對應的表格 '''
Base.metadata.create_all(engine)
''' 4.將 engine綁定(bind)到 Session 類別中'''
Session = sessionmaker(bind=engine)
''' 5.將這個已經與 engine 綁定的 Session 類別實例化，以開始進行與資料庫的互動'''
session = Session()

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

def getSession():
    return session





