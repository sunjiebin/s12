#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import threading,time
starttime=time.time()

class MyThread(threading.Thread):
    def __init__(self,n):
        super(MyThread,self).__init__()
        self.n=n
    def run(self):
        print('Thread',self.n,threading.current_thread(),threading.active_count())
        time.sleep(2)

t_objs=[]
for i in range(50):
    t=MyThread(i)
    t.start()
    t_objs.append(t)
    #t.join()  #如果join加在这里，则把并行变成了串行
'''下面的for循环线程实例列表，起到的作用就是
等待所有线程执行完毕，如果去掉下面的for部分，那么
脚本下面部分不会等待线程执行完毕，而是会和上面线程
一起并行执行，所以这时候打印总时间将不会是上面sleep
的2秒以上的时间，而是0点0几秒'''
for t in t_objs:
    t.join()

print('---all thread has finished---')
'''threading.current_thread()打印当前线程信息,
脚本本身就是主线程，会打印MainThread
threading.active_count()打印活跃的线程个数，前面的50个线程已经执行完毕了，所以这里只有1个活跃
线程，即脚本本身的主线程'''
print('cost time %s'%(time.time()-starttime),threading.current_thread(),threading.active_count())