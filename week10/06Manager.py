#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
'''进程间数据的共享，实际是将数据复制了多份到每个进程中，最后再汇总输出'''
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
        print(d)
        print(l)
