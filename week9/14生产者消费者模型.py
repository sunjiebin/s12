#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import queue,threading,time
q=queue.Queue(maxsize=10)
def producer():
    count=1
    while True:
        q.put('骨头%s'%count)
        print('生产骨头%s'%count)
        count += 1
        time.sleep(0.5)

def consumer(name):
    #while q.qsize()>0:
    while True:
        print('%s取到骨头%s并吃了它'%(name,q.get()))
        time.sleep(1)
p=threading.Thread(target=producer)
c=threading.Thread(target=consumer,args=('sun',))
c1=threading.Thread(target=consumer,args=('mi',))
p.start()
c.start()
c1.start()