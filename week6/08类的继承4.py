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
        self.friends.append(obj)
class man(people,relation):
    def sleep(self,obj):
        print('%s is sleeping with %s'%(self.name,obj.name))
class woman(people,relation):
    def get_birth(self):
        print('%s is born a baby'%self.name)
m1=man('sun', 18)
w1=woman('mi', 16)
m1.talk()
w1.name='helo'
m1.make_friends(w1)

print(m1.friends[0].name)
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
'''
终于弄明白了，当
self.friends.append(obj)  print(m1.friends[0].name)时，
self.friends.append(obj) 追加的是一个内存对象，是w1的内存地址，而不是一个固定的字符串，
所以当内存地址里面的变量变化时，那么这个self.friends也会跟着变。
m1.friends[0].name是从w1内存里面读出来的name.
1、当顺序为如下时
w1.name='helo'
m1.make_friends(w1)
print(m1.friends[0].name)
w1.name='helo'已经将w1的内存地址修改。所以此时
m1.make_friends(w1)时，下面函数中obj.name为w1.name，打印helo,
self.friends.append(obj)这里面传的w1，而此时w1.name已经是helo，所以也为helo
    def make_friends(self, obj):
        print('%s making friends with %s' % (self.name, obj.name))
        self.friends.append(obj)
此时obj.name=helo, m1.friends[0].name=helo
2、当顺序如下时
m1.make_friends(w1)
w1.name='helo'
print(m1.friends[0].name)
由于先执行了make_friends(w1),所以make_friends函数里面的obj.name此时是mi，
此时self.friends.append(obj)此时加载了w1的内存地址。
而后执行了w1.name='helo'，这时候将w1内存里面的name指向改为了helo
所以，对应的self.friends变量里面的self.friends[0].name也跟着变了。
self.friends[0].name == w1.name
这时候打印出来的m1.friends[0].name也就变成了helo
此时obj.name=mi,m1.friend[0].name=helo

当
self.friends.append(obj.name)  print(m1.friends[0])时，
self.friends.append(obj.name) 追加的是一个实例化的地址obj.name，即w1.name,这是一个固定的字符串
m1.friends[0]就是读取的w1.name
情景1：
w1.name='helo'
m1.make_friends(w1)
    def make_friends(self, obj):
    #obj.name=w1.name，所以打印出helo
        print('%s making friends with %s' % (self.name, obj.name))
     #这里面也是同理，传入的obj.name其实就是helo这个字符串，而不是一个变量   
        self.friends.append(obj.name)
#这里打印m1.friends[0]其实就是打印了obj.name，即helo
print(m1.friends[0])
此时obj.name=helo，m1.friends[0]=helo

情景2：
先执行m1.make_friends(w1)，再执行w1.name='helo'
m1.make_friends(w1)
    def make_friends(self, obj):
        #这里由于w1.name还未执行，所以obj.name还是原来的mi
        print('%s making friends with %s' % (self.name, obj.name))
        #同样的，这里的obj.name==原来的w1.name，也是mi
        所以此时的friends.append[0]的值已经是一个实例化的字符串mi
        self.friends.append(obj.name)
#此时再执行w1.name=helo，只是修改了people里面的self.name=helo，与self.friends[]没有任何关系了。
 w1.name='helo'   
#所以，此时的self.friends[0]打印出来的是mi
print(m1.friends[0])
此时obj.name=mi,m1.friends[0]=mi

'''




'''上面的类中，man和relation都没有定义name参数，但是它们
却都能够读到self.name，这是因为在执行在执行sun=man('sun',18)时，
先会将people里面定义的self.name,self.age实例化为self.name='sun'
relation类，people类里面的功能暂时只是加载到内存。
当执行sun.friends(mi)时，则将people里面实例化的self.name带到了
friend方法里面，所以friends里面的self.name就有了值。
'''