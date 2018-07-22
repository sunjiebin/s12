#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

class Role:
    n=123 #类变量，类变量存在于类的内存里面,大家共用的变量可以写这里，节省开销
    name='sun'   #如果实例变量和类变量一样时，会以实例变量为准
    n_list=[]
    def __init__(self,name,role2,weapon,life_value=100,money=1500):
        #构造函数，在实例化时做一些类的初始化工作
        self.name=name  #实例变量（静态属性），作用域是实例本身，而不是类
        self.role=role2
        self.weapon=weapon
        self.life_value=life_value
        self.money=money

    def shot(self): #类的方法，功能（动态属性）
        print('%s %s is shooting'%(self.role,self.name))
    def buy(self):
        print('%s buy %s'%(self.name,self.weapon))
#实例化类Role,即声明实例r1
r1=Role('sun','police','AK47')
#调用实例化r1里面的方法
r1.shot()
r1.buy()
#修改实例变量
r1.name='luo'
r1.shot()
#删除实例变量
#del r1.weapon
#r1.buy()

r2=Role('luo','police','m164a')
r2.buy()

#修改r1的n，这时候n只会存在于r1的内存里面，类里面的N1并未改变，所以并不会影响r2
r1.n='r1的n'
print(r1.n,r2.n)
'''修改类的n，则r2的构造函数里面没有n，所以会去类里面找这个n变量,所以r2的值为Role.n
而r1里面已经有n了，会优先找构造函数里面的n，所以为r1.n的值'''
Role.n='类变量n'
print(r1.n,r2.n)

#增加变量,这个变量只会存在于r1这个实例里面
r1.test='add'
print(r1.test)
#r2是调用不了test的，因为类里面并不存在
#print(r2.test)

#用列表的方式可以
r1.n_list.append('r1')
r2.n_list.append('r2')
#r1.n_list[0]='r1'

print(r2.n_list,r1.n_list)