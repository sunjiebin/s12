#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import queue

q=queue.LifoQueue(maxsize=3)
q.put(1)
q.put(2)
q.put(3)
print(q.get())
print(q.get())

q=queue.PriorityQueue()
q.put((-1,'helo'))
q.put((10,'sun'))
q.put((5,'mi'))
print(q.get())
print(q.get())
print(q.get())