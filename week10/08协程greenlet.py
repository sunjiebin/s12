#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
'''greenlet模块默认是没有的，需要用pip install greenlet安装
默认集成在gevent中'''
from greenlet import greenlet

def test1():
    print(12)
    gr2.switch()
    print(34)
    gr2.switch()

def test2():
    print(56)
    gr1.switch()
    print(78)
gr1=greenlet(test1)
gr2=greenlet(test2)
gr1.switch()
#gr2.switch