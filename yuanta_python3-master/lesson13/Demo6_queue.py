import threading
import time
import queue

class Worker(threading.Thread):
    def __init__(self, num, queue):
        threading.Thread.__init__(self)
        self.num = num
        self.queue = queue

    def run(self):
        while self.queue.qsize() > 0:
            job = self.queue.get()
            print('Worker %d: %s' % (self.num, job))
            if (self.num == 1):
                time.sleep(1)
            else:
                time.sleep(0.3)


my_queue = queue.Queue()
for i in range(10):
    my_queue.put('Data %d' % i)

worker1 = Worker(1, my_queue)
worker2 = Worker(2, my_queue)

worker1.start()
worker2.start()