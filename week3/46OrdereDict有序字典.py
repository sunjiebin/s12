#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''
在3.5及之前的版本，字典默认是无序的，
在3.5之后的版本，dict实际上是有序的了.
会依照key插入的顺序来编排，我当前版本是3.6的，所以下面的dic显示每次都是一样的，并没有实现无序显示。
另外，hash表的实现依然是无序状态
'''
dic=dict()
dic['a1']='c1'
dic['v2']='c2'
dic['a3']='c3'
print('dic的类型为{type}'.format(type=type(dic)))
print('{}的值为{}'.format('dic',dic))

#在3.6之前的版本，可以用下面的方法实现有序编排
# OrdereDict为有序字典
import collections
orderdic=collections.OrderedDict()
orderdic['k1']='v1'
orderdic['k2']='v2'
orderdic['k3']='v3'
print('orderdic的类型为',type(orderdic))
print(orderdic)
#更新字典，已经有值的键值对会被更新，如果不存在的则会新增
orderdic.update({'k4':'v4','k5':'v5'})
print(orderdic)
#去掉k4
orderdic.pop('k4')
print(orderdic)
#去掉一个不存在的键
print(orderdic.pop('abc','aa'))
#列表循环赋值，不会改变原来的有序字典
aa=orderdic.fromkeys(['a','b','c'],'dd')
print(aa)
#拿出最后一个元素，并从原字典中移除
print(orderdic.popitem())
print(orderdic)
#拿出最前面一个元素，并从原字典中移除
print(orderdic.popitem(last=False))
print(orderdic)
#新增键值对,默认值为None
orderdic.setdefault('k1')
print(orderdic)
#新增键值对，并指定值
orderdic.setdefault('k4','v4')
print(orderdic)
#移动键值对到最前面,默认last=True，即移到最后面
orderdic.move_to_end('k1',last=False)
print(orderdic)
