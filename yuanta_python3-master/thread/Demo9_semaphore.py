import threading
import time
import queue

class Worker(threading.Thread):
    def __init__(self, num, queue, semaphore):
        threading.Thread.__init__(self)
        self.num = num
        self.queue = queue
        self.semaphore = semaphore

    def run(self):
        while self.queue.qsize() > 0:
            job = self.queue.get()

            self.semaphore.acquire()

            print('Semaphore acquire by Worker %d' % self.num)

            print('Work %d %s' % (self.num, job))

            time.sleep(1)

            print('Semaphore release by Worker %d' % self.num)

            self.semaphore.release()

job_queue = queue.Queue()

for i in range(10):
    job_queue.put('Data %d' % i)

# 建立旗標
semaphore = threading.Semaphore(2)

worker1 = Worker(1, job_queue, semaphore)
worker2 = Worker(2, job_queue, semaphore)
worker3 = Worker(3, job_queue, semaphore)

worker1.start()
worker2.start()
worker3.start()



