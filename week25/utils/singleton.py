
class foo(object):
    instance=None
    def __init__(self):
        self.name='alex'
    @classmethod       # 定义类方法，这样就可以直接执行foo.get_instance()了，如果没有这个装饰器，就不能这么执行
    def get_instance(self):
        if  foo.instance:
            return foo.instance
        else:
            # 如果instance为空，则将foo()赋值给instance
            foo.instance=foo()
            #返回foo.instance,实际上就是返回的foo()这个函数
            return foo.instance
    def process(self):
        return '123'

# 实例化两个对象。
obj1=foo()
obj2=foo()
# 通过打印id发现两个实例申请了两块不同的内存空间，指向了两个对象。这就造成了内存浪费
print(id(obj1),id(obj2))

#单列模式
'''obj3第一次执行foo.get_instance()时，instance为空，此时执行foo.instance=foo(),这时候instance就有值了foo(),并且返回foo()。'''
obj3=foo.get_instance()
'''obj4第二层执行foo.get_instance()时，instance=foo()不为空，所以就直接返回了foo.instance，实际上就是返回了前面创建foo()'''
obj4=foo.get_instance()
# 两者得到的内存地址时一样的。
print(id(obj3),id(obj4))
# 通过上面的可以实现单例模式，但是不好的是必须通过foo.get_instance()的方式来创建

# 基于new方法的单例模式  永远用一个对象的实例，而不是创建多个对象
class foo2(object):
    instance=None
    def __init__(self):
        print('init')
        self.name='alex'

    '''在创建对象时，首先会先执行new方法，再执行init'''
    def __new__(cls, *args, **kwargs):
        print('new')
        if foo2.instance:
            return foo2.instance
        else:
            # object.__new__(cls,*args,**kwargs) 相当于foo2().
            foo2.instance=object.__new__(cls,*args,**kwargs)
            return foo2.instance

#通过上面的new函数，实现了类的单例模式。创建两个对象，实际上都是指向同一块内存空间。
obj=foo2()
obj2=foo2()
print(id(obj),id(obj2))