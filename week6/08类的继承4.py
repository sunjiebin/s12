#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

class people(object):
    def __init__(self,name,age):
        self.name=name
        self.age=age
        self.friends=[]

    def talk(self):
        print('%s is %s years old'%(self.name,self.age))

class relation(object):
    def make_friends(self, obj):
        print('%s making friends with %s' % (self.name, obj.name))
        self.friends.append(obj.name)
class man(people,relation):
    def sleep(self,obj):
        print('%s is sleeping with %s'%(self.name,obj.name))
class woman(people,relation):
    def get_birth(self):
        print('%s is born a baby'%self.name)
m1=man('sun', 18)
w1=woman('mi', 16)
m1.talk()
m1.make_friends(w1)
w1.name='helo'
'''这里一直不明白，当
self.friends.append(obj)  print(m1.friends[0].name)时，
w1.name不管怎么设置，不管放在哪，执行结果都是helo。

self.friends.append(obj.name)  print(m1.friends[0])时，
w1.name='helo'
m1.make_friends(w1)
这样就打印helo.
m1.make_friends(w1)
w1.name='helo'
这样就打印mi
'''
print(m1.friends[0])
#m1.sleep(w1)

'''上面的类中，man和relation都没有定义name参数，但是它们
却都能够读到self.name，这是因为在执行在执行sun=man('sun',18)时，
先会将people里面定义的self.name,self.age实例化为self.name='sun'
relation类，people类里面的功能暂时只是加载到内存。
当执行sun.friends(mi)时，则将people里面实例化的self.name带到了
friend方法里面，所以friends里面的self.name就有了值。
'''