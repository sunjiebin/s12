#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
from multiprocessing import Lock,Process
'''进程锁的主要作用是，当我们进程太多时，同时打印到一个终端上
有可能会出现打印的数据是乱的，前面的进程没打印完后面的进程又在
打印，结果输出的数据不是一条条完整的数据，加入锁可解决。
这个在python3里面可能不会出现，在python2的linux上有可能会出现'''
def f(l,i):
    l.acquire()
    print('hello world',i)
    l.release()
if __name__ == '__main__':
    lock=Lock()
    for num in range(100):
        Process(target=f,args=(lock,num)).start()

