import time
from multiprocessing import Pool

def job(n):
    time.sleep(1)
    sum = n * n;
    print(sum, end="")
    return sum

nums = [1, 2, 3, 4, 5, 6]

# 單執行緒
print('Single process:')
s = time.time()
for n in nums:
    job(n)

e1 = time.time()
print("\nSingle process time: %f\n" % (e1 - s))

# 同時並行
print('Concurrent process:')
s = time.time()
pool = Pool(6)  # 建立行程數量
result = pool.map(job, nums) # 進程齊發，最後取得總結果
pool.close()
pool.join()  # to wait for the pool
e2 = time.time()
print("\nConcurrent process time: %f\n" % (e2 - s))

print('result : ', result)