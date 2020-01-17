import threading
import time

class MyThread(threading.Thread):
    # 執行緒初始設置
    def __init__(self, num):
        threading.Thread.__init__(self)
        self.num = num

    # 執行緒 job
    def run(self):
        print('Thread:', self.num)
        time.sleep(1)


t = MyThread(10)
t.start()


