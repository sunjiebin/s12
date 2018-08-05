#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

from lib.aa import cat
class dog(object):
    '''这是一个测试类'''
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def fun(self):
        print('my name is %s'%self.name)
    '''让类可被直接调用'''
    def __call__(self, *args, **kwargs):
        print('running call',args,kwargs)
    '''返回类的返回值'''
    def __str__(self):
        return '%s'%self.name

d=dog('sun',18)
'''打印类的描述信息'''
print(d.__doc__)

'''__module打印模块的路径'''
e=cat('sun')
e.miao()
print(e.__module__)
'''class输出类的名称'''
print(e.__class__)
'''打印类里的所有属性和方法，不包括实例属性'''
print(dog.__dict__)
'''打印类里面的实例属性，不包括类属性，我们
前面只定义了name这个实例变量，所以这里就以字典
打印出name:sun，这个功能可用在当我们对这个类运行了
很久了，而且添加了很多方法变量等，可以用这个来查看
当前的变量'''
print(e.__dict__)

'''默认情况下是不能直接d()，也就是说实例是不能
直接被调用的，但在函数里面加上call后，就可以直
接调用函数了，相当于实例化类后，直接调用类，而
不是直接调用类里面的函数'''
d(1,2,3,name='sun',sex='M')
'''返回类的返回值，如果没有str函数，默认是返回的
内存地址'''
print(d)

