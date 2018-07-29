#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''需要重听'''

'''经典类在多继承上是有区别的'''
#class people: #经典类写法
class people(object):   #新式类的写法,推荐都用新式类
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        print('%s is eating...' % (self.name))

    def drink(self):
        print('%s is drinking....' % (self.name))
    def sleep(self):
        print('%s is sleepping...'%(self.name))

class relation(object):
    def make_friends(self,obj):
        print('%s is making friends with %s'%(self.name,obj.name))
'''
执行 m1.make_friends(m2)，相当于self就是m1,obj就是m2
print(m2.name)的值和print(obj.name)其实是一样的
上面语句中，self.name相当于m1.name,
obj.name相当于m2.name'''


'''如果我们想要在子类上增加传入的参数，可以用下面的写法，
先定义一个__init__构造函数，这时候__init__会覆盖父类的__init__,
相当于对父类的__init__进行了重构，所以，在定义子类的构造函数时，
也需要将父类的name,age都写进来，然后加上自己新增的money，并且在
构造函数体内要调用父类people的构造函数，这样就会执行父类的__init__,
父类里面的name,age则从子类的name,age变量中获取而来。
调用父类后，父类里面的__init__部分就会被继承到子类中。
'''
class man(people,relation):
    def __init__(self,name,age,money):
        #people.__init__(self,name,age)         #和下面的super一样，只是写法不一样
        '''建议用super，因为这样不用写父类的名称，如果以后父类名进行修改了，则不用改这里的people名称。
        在多类的继承时，只需要一条super就能够实现多类的继承了，super会根据man(people,relation)的顺序，
        先继承people，再继承relaition,如果用上面的写法，则需要写两条'''
        super(man,self).__init__(name,age)      #super代表我继承了父类函数，和上面的people写法意义是一样的
        self.money=money
        print('%s 带着%s块钱诞生了'%(self.name,self.money))
    def work(self):
        print('%s is working...'%(self.name))
    def sleep(self):
        people.sleep(self)
        print('man is sleeping...')



class woman(people):
    def shopping(self):
        print('%s is shopping...'%(self.name))




m1=man('sun',18,10)
#m1.work()
m2=woman('mi',16)
m2.shopping()

m1.make_friends(m2)


