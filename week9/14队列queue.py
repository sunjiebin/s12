#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import queue

q=queue.Queue(maxsize=3)
q.put('aa')
q.put('bb')
q.put('cc')
size=q.qsize()
print(size)
print(q.get())
#qsize判断队列大小，当里面没队列时为0
print(q.qsize())
'''用get每次执行一次就取一个值出来，当所有值取完时，程序就会卡住
等待新的值进来，如果不想在没有数据时被卡住，那么可以用get_nowait()'''
print(q.get())
print(q.get())
'''可以用false来指定不阻塞，即不卡住'''
print(q.get(block=False))
'''get支持timeout指定卡住的超时时间，超过时间就报错，而不是继续等待'''
print(q.get(timeout=3))
'''当没有数据时，也可用用get_nowait，会直接报错，而不是卡住，和get
的block=False一样'''
print(q.get_nowait())

'''同样的put也是如此，当添加的数据满时，也会卡住'''
q=queue.Queue(maxsize=3)
q.put(1)
q.put(2)
q.put(3)
q.put(4)
