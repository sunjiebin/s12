#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

with open('aa.txt','r') as f:
    for i in f:
        print(i)

with open('aa.txt','r') as f, \
     open('aa2.txt','r') as j:
    print(f.readlines())    #用readlines读出来的是列表形式
    print(j.readlines())