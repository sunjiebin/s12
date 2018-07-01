#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
#可命名元组
#默认元组只能通过游标的方式定位到元素，可命名元组可以对元素命名，这样就可以通过名称找到元素了
#这个提供的功能有点像坐标，如x,y,z
import collections
#创建一个类，相当于defaultdict类一样
name=collections.namedtuple('aa',['x','y','z'])
#通过这个类创建对象bb，里面x对应11，y对应22
bb=name(11,22,33)
print(bb.x)
print(bb.x+bb.y)
#指定x,y,z的对应值
cc=name(x='aa',z='bb',y=5)
print(cc)
print(cc.x)
print(bb.x+cc.y)

#查看我们创建的name类的方法
print(help(name))