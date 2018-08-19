#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import queue,multiprocessing
'''注意这个queue.Queue是一个线程队列，不是进程队列，所以
将这个线程产生的q传给子进程里面是会报错的。
正确的用法应该是用进程队列，即multiprocessing.Queue'''
def f(qq):
    qq.put([42,None,'helo'])
if __name__ == '__main__':
    #q=queue.Queue()    #这个是启动了一个线程queue,和进程queue不是一样的
    q=multiprocessing.Queue()
    p=multiprocessing.Process(target=f,args=(q,))
    p.start()
    print(q.get())
    p.join()