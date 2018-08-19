#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
'''gevent需要另外安装，默认没有'''
import gevent
def foo():
    print('running in foo')
    gevent.sleep(2)
    print('switch foo again')
def bar():
    print('running in bar')
    gevent.sleep(1)
    print('switch bar again')
def fun():
    print('running in fun')
    gevent.sleep(0)
    print('switch fun again')
gevent.joinall([gevent.spawn(foo),gevent.spawn(bar),gevent.spawn(fun)])