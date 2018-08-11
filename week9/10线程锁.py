#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
'''在python2里面，如果不加Lock线程锁，那么在执行下面代码时，
最后加出来的Num可能小于循环的次数50次。这个在py3里面不会出现。
加上这个锁之后，代表在这个线程执行时，其它线程要等待它执行完
毕后才可以再执行，实际上就相当于把线程变成串行来执行了'''
import time,threading
num=0
lock=threading.Lock()
def run(n):
    lock.acquire()
    global num
    num+=1
#    time.sleep(1)  #如果加上这个sleep，则要等50s程序才能执行完毕
    lock.release()

for i in range(50):
    t=threading.Thread(target=run,args=(i,))
    t.start()

print(num)
