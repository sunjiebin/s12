#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from multiprocessing import Pool,Process,freeze_support
import time,os

'''callback代表回调进程，即子进程执行完毕后，再由主进程进行回调，
这个回调是由主进程执行的，为什么不直接在子进程里面执行回调函数呢？
这里涉及到性能的优化，就比如当我子进程执行完成后，需要往sql里面写入
数据，这时候如果用子进程完成，那么每个进程就要建立一个连接再写入，
当进程数非常多的时候，就会建立很多个连接，那么这对数据库及程序端
都会增加很多的开销。如果用回调函数，则由于回调函数全部由同一个父进程
去完成的，所以只需要建立一次长连接，而不用建立多个连接'''

def foo(i):
    time.sleep(2)
    print('in process pid',os.getpid())
    return i+100
def bar(arg):
    print('exec done',arg,os.getpid())

if __name__ == '__main__':  #在windows中这段代码不能省，否则会报错
    freeze_support()
    '''定义三个进程池，即同时只会运行三个进程'''
    pool=Pool(3)
    print('主进程',os.getpid())
    for i in range(10):

        pool.apply_async(func=foo,args=(i,),callback=bar)   #apply_async代表异步执行
        #pool.apply(func=foo,args=(i,))   #注意apply是同步执行，即串行执行，所以看不出效果
    print('end')
    pool.close()
    pool.join() #注意这里的join这一步一定要写在close()的后面，且这一步不能少，否则不会执行子进程