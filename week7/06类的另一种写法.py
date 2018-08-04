#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''一切事务皆对象，所以类本身也是一个对象
class类是由type实例化产生的一个对象'''
class foo(object):
    def test(self):
        pass
f=foo()
'''打印实例化的对象f的类型'''
print(type(f))
'''打印类foo的类型，为type类'''
print(type(foo))

'''类的另一种写法，可以通过type来实现'''
def func(self):
    print('hello %s'%self.name)
def init(self,name,age):
    self.name=name
    self.age=age

'''f为类的名称，(object,)新式类，也可以写成()代表经典类，
类的名称talk,对应函数func，构造函数__init__，对应函数init
'''
f=type('f2',(object,),{'talk':func,'__init__':init})
a=f('sun',22)
print(type(f))
a.talk()