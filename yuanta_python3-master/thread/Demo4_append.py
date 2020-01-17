import threading
import time


def job(num):
    name = threading.current_thread().name
    print('%s thread:' % name, num)
    time.sleep(1)


threads = []
for i in range(5):
    threads.append(threading.Thread(target=job, args=(i,)))

for t in threads:
    t.start()
