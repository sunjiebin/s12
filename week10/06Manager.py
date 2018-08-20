#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
'''进程间数据的共享，实际是将数据复制了多份到每个进程中，最后再汇总输出'''
'''Manager用于进程间的通信，可以支持字典、列表、队列等多种方式在进程间传递数据'''
import os,multiprocessing
from multiprocessing import Manager
def f(d,l):
    d[os.getpid()]='dict'
    l.append(os.getpid())
    print(l)

if __name__ == '__main__':
    with Manager() as manager:
        d=manager.dict()
        l=manager.list(range(5))
        p_list=[]
        for i in range(10):
            p=multiprocessing.Process(target=f,args=(d,l,))
            p.start()
            p_list.append(p)
        for i in p_list:
            p.join()
        '''子进程里面的d,l能够被父进程读取，证明数据被传递了过来'''
        print(d)
        print(l)
