#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import queue
from multiprocessing import Queue,Process

def f(qq):
    qq.put([42,None,'helo'])
if __name__ == '__main__':
    q=Queue()
    p=Process(target=f,args=(q,))
    p.start()
    print(q.get())
    p.join()