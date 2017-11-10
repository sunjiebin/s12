#!/usr/bin/env python
# coding:utf-8
print '中文支持'
import sys

a=open('aa.txt','w')
a.write('hello\npython\n我是谁？\n我在哪？')
a.close()
b=open('aa.txt','r')
for i in b.readlines():
    print i