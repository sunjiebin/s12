#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import threading,time
'''setDaemon表示设置为守护线程，当线程变为守护
线程时，则主线程一旦执行完毕，守护线程就会立即结束，
而不论守护线程是否执行完毕，所以这个脚本的run函数
里面的sleep(2)会不生效，因为脚本主线程在2s内就执行
完了，所以直接杀掉了守护线程'''
def run(n):
    print('thread-%s'%n)
    time.sleep(2)
    print('weakup')

starttime=time.time()

for i in range(50):
    t=threading.Thread(target=run,args=(i,))
    t.setDaemon(True)
    t.start()

print('---thread done')