#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

'''一个模拟字典的类，将这个函数变成了一个类似于字典的实例，
可以用字典形式来设置key和value，可以更新字典，删除字典。
这个功能可以用于对字典做权限控制，如不允许更改字典的某个
键值对，不允许删除某个键值对，查找到某个key时做什么操作等'''
'''在py2.7里面还可以将实例变成列表，但在py3里面已经被去掉了'''
class foo(object):
    def __init__(self):
        self.dic={}
    def __getitem__(self, item):
        value=self.dic.get(item)
        print('getitem',item,value)

    def __setitem__(self, key, value):
        print('Setitem',key,value)
        self.dic[key]=value
        if key == 'sun':
            value='mi'
            print('%s不可被修改'%key)
    def __delitem__(self, key):
        print('delitem',key)

        if key == 'mi':
            print('%s不允许删除'%key)
        else:
            del self.dic[key]

obj=foo()
'''触发getitem'''
result=obj['k1']
'''触发setitem'''
obj['k2']='alex'
obj['k2']
'''触发delitem'''
del obj['k2']
del obj['mi']
'''sun定义的不可被修改'''
obj['sun']='luo'
obj['sun']
obj['k2']

