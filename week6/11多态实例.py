#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

'''多态：一种接口，多种实现
封闭是为了隐藏实现细节，继承可以扩展已存在的代码模块，
它们的目的都是为了代码的重用。而多太是为实现另一个目的
接口的重用。
'''

class Animal(object):
    def __init__(self,name):
        self.name=name
    @staticmethod
    def animal_talk(obj):
        obj.talk()
class dog(Animal):
    def talk(self):
        print('%s wangwang!'%self.name)

class cat(Animal):
    def talk(self):
        print('%s miaomiao~'%self.name)

c=dog('sun')
#c.talk()
d=cat('mi')
#d.talk()

'''可以通过下面的方法模拟实现多态
def animal_talk(obj):
    obj.talk()
animal_talk(c)
'''

Animal.animal_talk(c)
Animal.animal_talk(d)