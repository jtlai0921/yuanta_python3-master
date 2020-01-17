from lesson12.Dao import getSession, User

if __name__ == '__main__':
    session = getSession()

    user1 = User('user1')
    user2 = User('user2')
    
    session.add(user1)
    session.add(user2)

    # 提交到資料庫中儲存:
    session.commit()

    # 關閉 session:
    session.close()