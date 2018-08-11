#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import time,threading

def run(n):
    print('exec',n)
    time.sleep(2)

t1=threading.Thread(target=run,args=('t1',))
t2=threading.Thread(target=run,args=('t2',))
t1.start()
t2.start()