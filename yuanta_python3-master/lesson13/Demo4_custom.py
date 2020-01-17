import threading
import time

class MyThread(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self) # 將狀態傳給父類別
        self.num = num

    # 執行緒工作
    def run(self):
        name = threading.current_thread().name
        print('%s %d' % (name, self.num))
        time.sleep(1)

t = MyThread(21)
t.start()
