#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import collections
#创建一个counter类型的数据，会自动统计你输入字符出现的次数
#注意Counter的C必需大写，Counter类继承了字典的所有功能，所以字典的方法都可用于这个类
obj=collections.Counter('adsfdlkjdfalkjdflkj')
#这个看着像字典，但实际不是字典
print('type is',type(obj))
print(obj)
#取出字典排名前三个的元素
ret=obj.most_common(3)
print('most_common的值为',ret)
#
aa=obj.items()
print(type(aa),aa)
for bb,ee in aa:
    print('key is',bb,'value is',ee)

obj=collections.Counter('adsfdlkjdfalkjdflkj')
cc=obj.elements()
print(cc)
print(type(cc))
for d in cc:
    print(d)