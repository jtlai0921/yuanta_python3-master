# -*- coding: utf-8 -*-
from sqlalchemy import func, text
from orm.UserDAO import getSession, User

if __name__ == '__main__':

    session = getSession()

    rows = session.query(User)
    rows = session.query(User).order_by(User.id.desc())
    rows = session.query(User)[0:5]
    rows = session.query(User).group_by(User.name)
    '''列印出資料表內相同名字大於 2 個以上使用者名稱'''
    rows = session.query(User).group_by(User.name).having(func.count(User.name) > 4)
    rows = session.query(User.name)
    rows = session.query(User).filter_by(name='user1').all()  # .first()
    rows = session.query(User).filter(User.id == 1).filter(User.name == 'user1')
    rows = session.query(User).from_statement(text('select * from user where name=:name')).params(name='user1').all()
    rows = session.query(User).from_statement(text('select * from user where name=:name and id=:id')).params(name='user1', id=1).all()

    for row in rows:
        print(row)

    print(
        session.query(User).count()
    )

    # 關閉 session:
    session.close()
