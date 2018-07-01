#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

#单向队列只能单向进出，首先要导入queue模块
import queue
que=queue.Queue()
print(type(que))
#向队列中放入元素
que.put('123')
que.put('ab')
#查看队列是否已经满了
print(que.full())
print(que.empty())
#查看队列里的大小，里面有2个元素了则为2
print(que.qsize())
#取出队列里面的元素，由于是队列，所以一次只能去一个，只能依次一次次取
print(que.get())
print(que.get())
#指定队列大小为2,当输入的值大于2时，会出现运行等待
que2=queue.Queue(2)
que2.put('11,22,33')
print(que2.qsize())
que2.put('aa')
print('看对列是否已满',que2.full())
print('看队列是否为空',que2.empty())
que2.get()
que2.get()
print('看对列是否已满',que2.full())
print('看队列是否为空',que2.empty())
