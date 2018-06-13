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
print('s3 remove后的值为%s' %s3)
#s3.remove('sun')
#isdisjoint判断是否没有交集
s3=set(['sun','jie','bin'])
print(s3)
s4={'mi','sun','luo'}
s5={'luo','mi'}
print('判断s3是否与s4没有交集',s3.isdisjoint(s4))
print('判断s3是否与s5没有交集',s3.isdisjoint(s5))
#&交集 |合集 -补集
print('s3与s4交集',s3&s4)
print('s3与s4并集',s3|s4)
print('s3与s4补集,相当于减法',s3-s4)
#对称差分：找出两个集合中不相交的部分
print('s3与s4对称拆分%s'%(s3^s4))
#issubset判断是否是子集
print(s5.issubset(s4))
#issuperset判断是否是父集
print(s4.issuperset(s5))
#pop从集合里面拿出一个值并赋值给新的变量,原来的集合元素会减少。pop的取值是随机的
s6=s4.pop()
print('s6的值为',s6)
print('s4的值为',s4)
print('s5的值为%s' %(s5))
#symmetric_differenc求差集，即两个集合不相交的部分,与^是一样的
print(s4.symmetric_difference(s5))
print(s4^s5)
#symmetric_difference_update求差集并改变原有的变量
print('s4求差集前的值为',s4)
print(s4.symmetric_difference_update(s5))
print('s4求差集后的值为%s'%(s4))
#update更新元素到集合
s4.update(['jie','bin'])
print(s4)
