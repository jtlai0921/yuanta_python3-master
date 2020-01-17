from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

class Num:
    value = 0.0

if __name__ == '__main__':
    num = Num()
    arr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # num = Value('d', 0.0)
    # arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])