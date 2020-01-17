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


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))

addresses = relationship("Address", back_populates="user")
user = relationship("User", back_populates="addresses")

addresses = relationship("Address", backref="user")

if __name__ == '__main__':
    ''' 1.建立 engine '''
    engine = create_engine('sqlite:///demo.db', echo=False)
    ''' 2.在資料庫內建立起相對應的表格 '''
    Base.metadata.create_all(engine)
    ''' 3.將 engine綁定(bind)到 Session 類別中'''
    Session = sessionmaker(bind=engine)
    ''' 4.將這個已經與 engine 綁定的 Session 類別實例化，以開始進行與資料庫的互動'''
    session = Session()

    u1 = User()
    a1 = Address()
    print(a1.user)


    # 提交到資料庫中儲存:
    session.commit()

    # 關閉 session:
    session.close()