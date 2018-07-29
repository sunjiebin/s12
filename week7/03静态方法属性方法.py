#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

#静态方法
'''静态方法只是名义上归类管理，实际访问不了类或实例里面的属性'''
class Dog(object):
    def __init__(self,name):
        self.name=name
        print('%s eat'%self.name)
    @staticmethod
    def eat(obj):   #实际上变成一个函数了
        print('%s is eat %s'%(obj.name,'pig'))
#d=Dog('sun')
#c=Dog('mi')
#d.eat(c)

#类方法
'''类方法只能访问类变量，不能访问实例变量
在构造函数中定义了self.name，但我们调用时发现调用不了，
而在类里面定义的name，我们就可以调用，也就是说，实例里
面的变量定义已经失效了。
'''
'''这个功能用处在于，我们定义的类里面，有很多方法，
某一个方法我们想让它的参数值是固定的，不受外界影响，
则可以用这个功能
例如:朝鲜是不允许改国籍的，其它国家都可以改。我们定
义这样一个类之后，关于朝鲜的方法就可以把它的国籍写死
'''

class Pig(object):
    name='huazai'
    food='balana'
    def __init__(self,name,food):
        self.name=name
        self.food=food
    @classmethod        #加上类方法后，构造函数里面定义的name,food变量均失效了，取而代之的是类里面定义的属性
    def eat(self,action):
        print('%s is %s %s'%(self.name,action,self.food))
    def eat2(self,action):     #同样的函数，没有类方法，则构造函数里面的属性生效，优先级高于类里面的属性定义
        print('%s is %s %s'%(self.name,action,self.food))
#e=Pig('sun','apple')
#e.eat('eating')
#e.eat2('eating')

#静态属性
'''
把一个方法变成一个静态属性
在调用的时候就不能传参数了

'''
class cat(object):
    name='huazai'
    food='balana'
    def __init__(self,name,food):
        self.name=name
        self.food=food
        self.action='playing'
    @property   #静态属性方法
    def eat(self):
        print('%s is %s %s'%(self.name,self.action,self.food))
    def play(self):
        print('%s is playing with %s'%(self.name,self.food))

    '''注意
    1、这里的@eat中的eat是上面的eat的名称，由于解析是自上而下的，
    所以在这个@eat上面必需要有一个eat以供解析，否则会报错。
    2、@eat。setter下面一行必需是要装饰的函数，不能是别的内容，
    注释都不行，如果注释写的@eat.setter下一行也是会报语法错误的'''
    @eat.setter     #更新属性
    def eat(self,action):
        print('---eat.setter...')
        print('%s is %s %s'%(self.name,action,self.food))
        #用setter是可以改变原来eat里面的属性的，如下就改变了action,food的值
        self.action=action
        self.food='balana'
    '''删除属性，默认情况下是不可以执行del f.eat删除属性的，可以用下面的方法删除'''
    @eat.deleter
    def eat(self):
        del self.action
        print('删除了action')
f=cat('sun','milk')
f.eat
#属性方法默认是不能给eat赋值的，我们需要执行下@eat.setter才可以
f.eat='eating'
'''
再次执行f.eat会发现结果和上一次执行的f.eat不一样了。因为在上条
命令中,f.eat='eating'，已经将action变成了eating，同时将food变成了
balana，所以后面再执行eat结果就是新赋值的结果了。
'''
f.eat
#执行删除属性，删除里面的self.action
del f.eat
#由于删除了self.action，所以下面的执行就报错了。
f.eat