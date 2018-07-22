#!/usr/bin/env python
# Python version: python3
# Auther: sunjb


class cs:
    def __init__(self,name,value,blood):
        self.name=name
        self.value=value
        self.__blood=blood  #私有属性，无法通过实例直接修改或调用这个属性
    def __shoot(self):
        self.__blood=50
        print('you blood %s'%(self.__blood))
    def youname(self):
        print('you name is %s'%(self.name))
    def shoot_status(self):
        self.__shoot()  #可在内部调用私有方法
        print('blood is %s'%(self.__blood)) #可在内部调用私有属性

test=cs('sun','person','100')
print(test.value)
#直接调用__blood会报错，读取和修改均不行
#print(test.__blood)
#非私有属性可以直接更改
test.name='aa'
#调用方法youname
test.youname()
#私有方法__shoot无法被调用
#test.__shoot()
#可以通过类里面的其它方法来取出
test.shoot_status()