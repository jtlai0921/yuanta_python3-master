# -*- coding: utf-8 -*-
from orm.UserDAO import getSession, User

if __name__ == '__main__':
    session = getSession()

    affected_rows = session.query(User).filter_by(id=1).delete()
    print('Affected rows:', affected_rows)

    for r in session.query(User):
        print(r)

    # 提交到資料庫中儲存:
    session.commit()

    # 關閉 session:
    session.close()