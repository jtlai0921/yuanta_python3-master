import time
import threading
from multiprocessing import Process, Pipe

def f(conn):
    time.sleep(1)
    conn.send([42, None, 'hello'])
    print('conn1 send')
    conn.close()

def job():
    conn1, conn2 = Pipe()
    p = Process(target=f, args=(conn1,))
    p.start()
    print('conn2 ready')
    print('conn2 recv', conn2.recv())   # prints "[42, None, 'hello']"
    p.join()

if __name__ == '__main__':
    t = threading.Thread(target=job)
    t.start()
    print('Wait...')
    t.join()
    print('Done.')
