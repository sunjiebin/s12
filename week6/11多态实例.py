#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

'''多态：一种接口，多种实现
封闭是为了隐藏实现细节，继承可以扩展已存在的代码模块，
它们的目的都是为了代码的重用。而多太是为实现另一个目的
接口的重用。
'''
'''
通过@staticmethod静态化之后，实际上下面的def就变成了一个函数，
和类里面其它方法不一样了，所以self也并不需要了。这个叫静态方法
'''
'''静态方法只是名义上归类管理，实际在静态方法里面访问不到类或实例中的任何属性'''
class Animal(object):
    def __init__(self,name):
        self.name=name
    @staticmethod
    def animal_talk(obj):
        obj.talk()
        #已经不能访问self.name
        #print(self.name)
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