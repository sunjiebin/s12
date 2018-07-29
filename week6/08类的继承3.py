#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

class people(object):
    def __init__(self,name,age):
        self.name=name
        self.age=age
        print('in people')
    def Age(self,obj):
        print('%s is %s'%(self.name,self.age))
        print('%s is %s'%(obj.name,obj.age))
class dog(object):
    def __init__(self,name,age):
        self.name=name
        self.age=age
        print('in dog')
    def wang(self):
        print('%s are wangwangwang！'%self.name)
'''在relation中，加上super，让relation也调用'''
class relation(object):
    def __init__(self,name,sex,age):
        self.sex=sex
        super(relation, self).__init__(name,age)
        print('in relation')
    def friends(self,obj):
        print('the %s is %s making friends with %s'%(self.sex,self.name,obj.name))

'''man继承了relation,people两个类，构造函数查找会
先relation的init部分查找配置，找到了就不再加载people中的init部分'''
class man(relation,dog,people):
    def work(self):
        print('%s is work'%self.name)

m1=man('sun','M',28)
m2=man('mi','F',26)
m1.friends(m2)
m1.Age(m2)
m1.wang()

'''在上面的函数中，如果
man(relation,dog)  
relation(object)
super(relation, self).__init__(name,age)
那么relation中的super将会加载dog类。
加载过程将是man-->relation-->dog
people类将不会被加载，所以调用people里面的
方法会报错。
如果：
man(relation,dog)
relation(people)
即relation中指定继承了people，那么
relation中的super将会加载people类，
同时man里面会加载dog类，所以执行过程为
man-->relation-->people-->dog
所以people,dog类都会被加载，man可以调用
people里面的方法
'''