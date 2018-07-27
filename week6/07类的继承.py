#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''可以在类里面定义子类，子类会继承父类的属性和方法
但是不同的子类之间不可以相互调用'''
class people:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        print('%s is eating...' % (self.name))

    def drink(self):
        print('%s is drinking....' % (self.name))
    def sleep(self):
        print('%s is sleepping...'%(self.name))


class man(people):
    def work(self):
        print('%s is working...'%(self.name))
    def sleep(self):
        people.sleep(self)
        print('man is sleeping...')
class woman(people):
    def shopping(self):
        print('%s is shopping...'%(self.name))

d=man('sun',18)
#调用父类里面的方法
d.eat()
#调用自己的方法
d.work()
#可在类里面直接调用父类的方法
d.sleep()


e=woman('luo',18)
e.drink()
#woman不能调用man里面的方法
#e.work()
