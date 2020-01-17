# -*- coding: utf-8 -*-
import datetime
import hashlib
from sqlalchemy import create_engine, DateTime, Column, Integer, String, func, text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

# 用來映對 Python 類別與資料庫表格之間的關聯
Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    # 在父類別中透過 relationship() 方法來引用子表的類別集合
    children = relationship("Child")
    def __str__(self):
        return "Parent('{}')".format(
            self.id
        )

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    # 在子表類別中透過 foreign key (外键)引用父表類別的参考欄位變數
    parent_id = Column(Integer, ForeignKey('parent.id'))
    parent = relationship("Parent")
    def __str__(self):
        return "Child('{}')".format(
            self.id
        )


if __name__ == '__main__':
    ''' 1.建立 engine '''
    engine = create_engine('sqlite:///demo.db', echo=False)
    ''' 2.在資料庫內建立起相對應的表格 '''
    Base.metadata.create_all(engine)
    ''' 3.將 engine綁定(bind)到 Session 類別中'''
    Session = sessionmaker(bind=engine)
    ''' 4.將這個已經與 engine 綁定的 Session 類別實例化，以開始進行與資料庫的互動'''
    session = Session()

    # c1 = Child()
    # c2 = Child()
    # c3 = Child()
    # c4 = Child()
    # session.add(c1)
    # session.add(c2)
    # session.add(c3)
    # session.add(c4)
    #
    # p1 = Parent()
    # p2 = Parent()
    # p1.children = [c1, c3, c4]
    # p2.children = [c1, c2]
    #
    # session.add(p1)
    # session.add(p2)

    for p in session.query(Parent):
        print(p, end=':')
        for c in p.children:
           print(c, end=' ')
        print()

    for c in session.query(Child):
        print(c, ":", c.parent)


    # 提交到資料庫中儲存:
    session.commit()

    # 關閉 session:
    session.close()