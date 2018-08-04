#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''
hasattr 判断一个对象里面是否有字符串对应的方法
getattr 判断字符串去获取对象里面对应的方法的内存地址
setattr 根据传入的字符串，修改对应字符串的值，如果类中不存在字符串，则新增属性
delattr 删除字符串对应的函数或属性
'''
def bulk(self):
    print('%s wang wang wang!!!'%self.name)

class dog(object):
    def __init__(self,name):
        self.name=name
    def eat(self,food):
        print('%s is eating %s'%(self.name,food))


d=dog('sun')
d.eat('apple')

func='eat'
choice=input()
print(hasattr(d,func))
print(getattr(d,func))
'''这里输入如果是一个存在的函数名eat，那么会执行
getattr(d,choice),即d=d.eat,d('agg')相当于d.eat('agg')
当这里输入的是一个变量名name时，hasattr条件判断成立，
那么d=d.name，而d.name=self.name='sun',所以这时候
执行d('agg'）是会报错的，因为d已经成为一个字符串sun了。
不具备()的属性了。
'''
if hasattr(d,choice):
    e=getattr(d,choice)
    print(e)
#    d('agg')
    '''如果要改变里函数里面属性的值，用setattr即可'''
    setattr(d,choice,'mi')
    '''用getattr可以接choice变量，如果用print(d.name)那么name就写死了'''
    print(getattr(d,choice))
    #print(d.name)
    '''删除对象里面的属性值，删除后再打印就报错了'''
    delattr(d,choice)
#    print(d.name)
else:
    setattr(d,choice,bulk)
    # d.talk(d)
    v=getattr(d,choice)
    v(d)
    '''如果函数属性不存在，则会添加一个属性'''
    setattr(d,choice,22)
    print(getattr(d,choice))

#e=dog('sun')
#func2='oh'
'''将bulk方法装入到类里面'''
'''下面相当于e.func2=bulk，即e.oh()就是执行的bulk()'''
#setattr(e,func2,bulk)
'''这样执行self没有被传进去，所以我们要(e)把自己传进去，不然没有self.name'''
#e.oh(e)