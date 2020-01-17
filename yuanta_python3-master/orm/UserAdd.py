# -*- coding: utf-8 -*-
from orm.UserDAO import getSession, User

if __name__ == '__main__':

    session = getSession()

    user = User('user1')
    print(user)
    print('Mapper:', user.__mapper__)

    session.add(user)

    rows = session.query(User)

    for row in session.query(User):
        print(row)

    #session.rollback()  # 資料庫回到新增 user1 之前的狀態

    print('count:', session.query(User).count())

    # 提交到資料庫中儲存:
    session.commit()

    # 關閉 session:
    session.close()