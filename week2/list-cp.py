#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

'''用户列表的浅cp演示'''

'''默认的浅cp'''
# aa=['sun','jie','bin',['luo','mi'],]
# print(aa)
# bb=aa.copy()
# print(bb)
#
# aa[aa.index('bin')]='biao'
# print(aa)
# print(bb)
#
# aa[3][0]='xiao'
# print(aa)
# print(bb)

'''深cp演示'''
aa=['sun','jie','bin',['luo','mi'],]
import copy
cc=copy.copy(aa) #bb=aa.copy()的效果相同
dd=copy.deepcopy(aa) #深拷贝
#修改嵌套列表里面的值
aa[3][1]='mimi'
#aa[aa.index(['xiao','mi'])][aa[aa.index(['xiao','mi'])].index('mi')]='mimi' 和上面的aa[3][1]结果相同
print(aa)
print(cc)
print(dd)