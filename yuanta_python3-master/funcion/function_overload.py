import time;

def new_print(str):
    file = open("log.txt", 'a') # a:append
    # 使用 strftime 方法格式化日期，：
    ds = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    file.write(ds + " -> " + str + "\n")


def overload_print():
    global print
    print = new_print


overload_print()
print('Hello')

