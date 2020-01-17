import threading
import time

def job(a, b):
    print('thread:', (a+b))
    time.sleep(1)

x = 10
y = 20
t = threading.Thread(target=job, args=(x, y,))
t.start()