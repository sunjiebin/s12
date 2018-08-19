#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import threading,queue,multiprocessing
'''注意进程和线程的区别
子线程可以共享父线程的数据，所以在父线程里面定义的q可以被子线程函数f读到，
子进程和父进程之间是内存的复制，两个进程之间的内存是独立的，之间的数据是
不共享的，所以子进程是无法读到父进程的q的'''
def f():
    q.put('123')
if __name__ == '__main__':
    q=queue.Queue()
    '''创建一个子线程p，子线程调用了函数f'''
    #p=threading.Thread(target=f,)
    '''创建一个子进程p，这时候上面定义的q是无法到子进程里面去的'''
    p=multiprocessing.Process(target=f,)
    p.start()
    print(q.get())
    p.join()
