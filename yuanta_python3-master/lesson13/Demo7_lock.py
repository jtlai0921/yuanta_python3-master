import threading
import time
import queue

class Worker(threading.Thread):

    def __init__(self, num, queue, lock):
        threading.Thread.__init__(self)
        self.num = num
        self.queue = queue
        self.lock = lock

    def run(self):
        while self.queue.qsize() > 0:
            job = self.queue.get()
            # 取得 lock
            self.lock.acquire()
            print('Lock acquire by Worker %d' % self.num)

            print('Work %d %s' % (self.num, job))

            time.sleep(1)

            print('Lock release by Worker %d' % self.num)
            print('--------------------------------------')
            # 釋放 lock
            self.lock.release()

job_queue = queue.Queue()

for i in range(10):
    job_queue.put('Data %d' % i)

# 建立 lock
lock = threading.Lock()

worker1 = Worker(1, job_queue, lock)
worker2 = Worker(2, job_queue, lock)

worker1.start()
worker2.start()
