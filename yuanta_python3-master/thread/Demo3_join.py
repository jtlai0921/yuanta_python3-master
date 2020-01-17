import threading
import time

def job():
    for i in range(5):
        print('thread:%d' % i)
        time.sleep(1)

t = threading.Thread(target=job)

t.start()

for i in range(3):
    print('Main:%d' % i)
    time.sleep(1)

# 等待持執行緒結束
t.join()

print('Done!')

