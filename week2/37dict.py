#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
# 字典小练习，将aa列表中小于66的值分到dic字典中的K1中，大于66的分到k2中
aa=[11,22,33,44,55,66,77,88,99,]

less=[]
more=[]
dic={}
for i in aa:
    if i<66:
      less.append(i)
    else:
        more.append(i)
dic={'k1':less,'k2':more}
print(dic)

dic2={}
for i in aa:
    if i<66:
        if 'k1' in dic2.keys():
            dic2['k1'].append(i)
        else:
            dic2['k1']=[i,]
    else:
        if 'k2' in dic2.keys():
            dic2['k2'].append(i)
        else:
            dic2['k2']=[i,]
print(dic2)