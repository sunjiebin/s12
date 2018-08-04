#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''new是函数里面的内置方法，是用来创建实例的，
new的init之前执行，如果没有new,就不会有init，
平时没有写new，但new其实一直存在。当我们手动
写上new时，实际是对内置的new进行重构。return
不能省，如果去掉则只会执行new，而不会再执行
init构造函数了
我们在实例化之前，如果想做一些操作，那么就可
以用new函数来实现'''
class func(object):
    def __init__(self,name):
        self.name=name
        print('func init %s'%self.name)
    def __new__(cls, *args, **kwargs):
        print('func new')
        '''new先于Init执行，下面语句如果注释，则不会init
        这里其实就是去继承父类的new方法'''
        return object.__new__(cls)
f=func('sun')
