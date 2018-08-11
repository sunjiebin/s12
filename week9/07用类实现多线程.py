#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import threading

class MyThread(threading.Thread):
    def __init__(self,n):
        super(MyThread,self).__init__()
        self.n=n
    def run(self):
        print('class thread',self.n)
t1=MyThread('t1')
t2=MyThread('t2')
t1.start()
t2.start()
