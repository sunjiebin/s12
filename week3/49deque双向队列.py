#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

#单向对列，左边进，右边出
#双向对列，两边都可进出
import collections
queue=collections.deque()
queue.append(2)
print(queue)
queue.extend([1,2,3])
print(queue)
queue.insert(3,'a')
print(queue)
print(queue.index('a'))
queue.pop()
print(queue)
queue.popleft()
print(queue)
queue.remove('a')
print(queue)
queue.extend([11,22,33])
print(queue)
queue.reverse()
print(queue)
queue.rotate(3)
print(queue)