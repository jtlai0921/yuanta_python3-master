import threading
import time
import queue

class Worker(threading.Thread):

    def __init__(self, num, queue):
        threading.Thread.__init__(self)
        self.num = num
        self.queue = queue

    def run(self):
        # 判斷佇列中還有沒有 job ?
        while self.queue.qsize() > 0:
            # 取得 job
            job = self.queue.get()
            # 處理 job
            print("Worker %d: %s" % (self.num, job))
            # 能者多勞判斷
            if(self.num == 1):
                time.sleep(1)
            else:
                time.sleep(0.3)

# 建立佇列
job_queue = queue.Queue()

# 將資料放入佇列
for i in range(10):
    job_queue.put("Data %d" % i)



worker1 = Worker(1, job_queue)
worker2 = Worker(2, job_queue)

worker1.start()
worker2.start()