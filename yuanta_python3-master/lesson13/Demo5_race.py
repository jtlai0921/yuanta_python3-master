import threading
import time

class Race(threading.Thread):
    def __init__(self, num):
        threading.Thread.__init__(self)  # 將狀態傳給父類別
        self.num = num

    # 執行緒工作
    def run(self):
        name = threading.current_thread().name
        for i in range(self.num):
            print('%s 跑了 %d 步' % (name, i))

step = 1001;
r1 = Race(step)
r2 = Race(step)
r1.name = '烏龜'
r2.name = '兔子'
r1.start()
r2.start()

r1.join()
r2.join()

print('Game over !')