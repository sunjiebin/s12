#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

class cat(object):
    '''这是一个测试类'''
    def __init__(self,name):
        self.name=name

    def miao(self):
        print('%s miaomiao'%self.name)