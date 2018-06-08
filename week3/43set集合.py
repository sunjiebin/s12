#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

#创建集合对象
# set 1、访问速度快 2、解决了重复的问题
s1=set()
s1.add('alex')
print(s1)
s1.add('alex2')
print(s1)
s1.add('alex')
print(s1)
#也可以直接给set变量赋值,注意是列表形式
s2=set(['sun','jie','sun','bin',])
print(s2)
#diffrence比较和老的集合有什么不同，并将不同之处生成一个新的集合
s2.difference(['sun','bin'])
#打印发现s2并没有改变
print(s2)
#赋值给s3
s3=s2.difference(['sun','bin'])
#打印发现s3的结果正是两者不一样的地方
print(s3)
print(s2)
#下面是错误的写法，python并不会报错
s2.difference_update('sun')
print(s2)
#正确的写法如下
s2.difference_update(['sun'])
print(s2)
