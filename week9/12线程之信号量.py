#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import threading,time
'''threading.BoundedSemaphore(5)代表同时只能有5个线程并行，
相当于只有5把钥匙，执行完一个之后就释放一把钥匙，然后再加入
一个线程。脚本打印效果是每次只显示5个，实际上如果每个线程
执行的时间不一样的，就不会这样打印，正确的理解是每完成一个
线程就会新加入一个线程，保证同时只有5个线程就行'''
def run(n):
    #调用信号量控制
    semaphore.acquire() #如果不调用则信号量控制不生效
    time.sleep(1)
    print('thread', n)
    #释放锁
    semaphore.release()    #如果不释放，则锁一直占用，程序会一直挂起
#开启信号量为5，即只允许5个线程并行
semaphore=threading.BoundedSemaphore(5)
for i in range(20):
    t=threading.Thread(target=run,args=(i,))
    t.start()
while threading.active_count() != 1:
    pass
else:
    print('done')