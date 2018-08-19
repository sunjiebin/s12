#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
'''启动和进程和启动多线程的语法类似，在多进程中，
还可以启动多线程'''
import time,multiprocessing,threading
def thread_run():
    print(threading.get_ident())
def run(name):
    time.sleep(2)
    print('hello',name)
    t=threading.Thread(target=thread_run)
    t.start()
if __name__ == '__main__':
    for i in range(10):
        p=multiprocessing.Process(target=run,args=('bob',))
        p.start()

