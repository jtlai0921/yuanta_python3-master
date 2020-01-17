import time
import threading
from multiprocessing import Pool

def job(n):
    time.sleep(1)
    sum = n * n;
    print(sum, end="")
    return sum

nums = [1, 2, 3, 4, 5, 6]

# 多執行緒
print('Threading process:')
s = time.time()

threads = []
for n in nums:
    threads.append(threading.Thread(target=job, args=(n,)))

for t in threads:
    t.start()

for t in threads:
    t.join()

e1 = time.time()
print("\nExecution time in single process: %f\n" % (e1 - s))


# 同時並行
s = time.time()
print('Concurrent process:')
pool = Pool(6)  # 建立行程數量
result = pool.map(job, nums) # 進程齊發，最後取得總結果
pool.close()
pool.join()  # to wait for the pool
e2 = time.time()
print("\nExecution time in concurrent: %f\n" % (e2 - s))

print('result : ', result)
