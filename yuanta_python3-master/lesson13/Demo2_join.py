import threading
import time

def gas():
    print('瓦斯工人送瓦斯')
    for i in range(5):
        print('送瓦斯中: ', i)
        time.sleep(1)
    print('瓦斯工人送到了')

print('爸爸下班回家')
print('爸爸想洗熱水澡')
print('爸爸發現沒熱水')
print('爸爸打電話叫瓦斯')
t = threading.Thread(target=gas)
t.start()
t.join()
print('爸爸洗熱水澡')
print('爸爸洗完了')
