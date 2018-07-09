#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''高阶函数就是在参数里面还引用了变量或函数
如下，定义了z为abs方法'''
def high(x,y,z):
    result=z(x)+z(y)
    return result

print(high(-1,-10,abs))