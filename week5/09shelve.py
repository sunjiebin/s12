#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

'''shelve模块是一个简单的k,v将内存数据通过文件持久化的模块，
 可以持久化任何pickle可支持的python数据格式，它相对于pickle
 而言，能够多次dump，还可以通过字典的方式来取出'''

import shelve,datetime
d=shelve.open('shelve_test')
dic={'a':'b','c':2}
lst=[1,2,3,3,]
d['list']=lst
d['dict']=dic
d['date']=datetime.datetime.now()
d.close()
'''执行后会自动生成三个文件，bak/dat/dir'''
#这个方式其实是存的一个字典，所以可以用get把值取出
d=shelve.open('shelve_test')
print(d.get('list'))
print(d.get('date'))
d.close()