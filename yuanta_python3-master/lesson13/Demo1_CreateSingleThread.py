import threading
import time

# 執行緒工作
def job():
    for i in range(5):
        name = threading.current_thread().name
        print("%s: %d" % (name, i))
        time.sleep(1)

def job2(a, b):
    name = threading.current_thread().name
    print("%s: %d" % (name, (a+b)))
    time.sleep(1)

x = 10;
t = threading.Thread(target=job2, args=(x, 20,))
t.name = '林董'
t.start()
