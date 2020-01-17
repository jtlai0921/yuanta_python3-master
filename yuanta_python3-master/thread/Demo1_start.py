import threading
import time

# 執行緒工作
def job():
    for i in range(5):
        # 取得執行中的執行緒名稱
        name = threading.current_thread().name
        print('%s thread:%d' % (name, i))
        time.sleep(1)

# 建立執行緒
t = threading.Thread(target=job)
# 設定執行緒名稱
#t.name = 'mythread'

# 啟動執行緒
t.start()




