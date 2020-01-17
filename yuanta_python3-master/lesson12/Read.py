from sqlalchemy import func, text

from lesson12.Dao import getSession, User

if __name__ == '__main__':
    session = getSession()

    users = session.query(User)\
        .from_statement(text('select * from user where name=:name'))\
        .params(name='user1')\
        .all()

    for user in users:
        print(user)

    # 關閉 session:
    session.close()
