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
#intersection取交集
s3={'sun','jie','mi'}
print(s2.intersection(s3))
print(s3.intersection(['jie','mi']))
print(s2)
print(s2.intersection(['jie']))
print(s3)
s3.intersection_update(['sun','mi'])
print('s3取交集后更新值为 %s'%(s3))
#discard删除元素，如果元素不存在不会报错
#注意这样写(['mi'])是错误的
s3.discard('mi')
print('s3 discard删除之后的值为',s3)
s3.discard('mi')
#remove删除元素
s3.add('bin')
print(s3)
s3.remove('sun')
print('s3 remove后的值为',s3)
#s3.remove('sun')
