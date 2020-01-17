from sqlalchemy import func, text

from lesson12.Dao import getSession, User

if __name__ == '__main__':
    session = getSession()
    affected_rows = session.query(User).filter_by(id=1).update({'id': 1, 'name': 'sqlalchemy'})
    print('Affected rows:', affected_rows)

    for r in session.query(User):
        print(r)

    # 關閉 session:
    session.close()
