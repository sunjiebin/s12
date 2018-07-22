#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

#析构函数用于在实例结束后自动执行的，通常用于一些收尾工作，如关闭打开的数据库，删除临时文件等
class cs:
    def __init__(self,user,role,gun='ak47'):
        self.name=user
        self.role=role
        self.weapon=gun
    def shoot(self):
        print('a %s %s is shooted by %s'%(self.role,self.name,self.weapon))
    def __del__(self):
        print('%s 彻底的死干净了'%self.name)
#声明一个实例user1
user1=cs('sun','policy')
user1.shoot()

user2=cs('luo','chief','砍刀')
user2.shoot()
#我们可以用del来删除实例，这时候就会触发析构函数
del user2
#user1没有被手动删除，所以会在整个脚本运行完毕后，自动删除时执行析构函数
