#! /usr/bin/env python
# Python version: python3
# Auther: sunjb
'''使用defaultdict需要导入collections模块'''
import collections
bb=[11,22,3,44,5,66,77,88]
#设置默认字典值的类型为list列表
dic=collections.defaultdict(list)
dic['k1'].append(5)
print(dic)

for i in bb:
    if i<66:
        dic['k1'].append(i)
    else:
        dic['k2'].append(i)
print(dic)

#设置默认字典的类型为set集合
dicset=collections.defaultdict(set)
for j in bb:
    dicset['j1'].add(j)
print(dicset)
dicset.update({'k1':'df','j1':'dfdf'})
print(dicset)