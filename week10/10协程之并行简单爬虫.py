#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from urllib import request
from gevent import monkey
import gevent,time

monkey.patch_all()

def f(url):
    print('get: %s'%url)
    resp=request.urlopen(url)
    date=resp.read()
    print('%d bytes recived from %s'%(len(date),url))
urls = ['https://www.python.org','https://www.baidu.com','https://www.51cto.com',]

stime=time.time()
for i in urls:
    f(i)
print('同步用时：',time.time()-stime)

async_time=time.time()

gevent.joinall([
    gevent.spawn(f,'https://www.python.org'),
    gevent.spawn(f,'https://www.baidu.com'),
    gevent.spawn(f,'https://www.51cto.com'),
])
print('异步用时：',time.time()-async_time)
