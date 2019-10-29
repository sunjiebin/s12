#!/usr/bin/env python3
# Auther: sunjb

#适配器模式
'''
将一个类的接口转换成客户希望的另外一个接口。使得原本由于接口不兼容而不能一起工作的那些类可以一起工作。
应用场景：希望复用一些现存的类，但是接口又与复用环境要求不一致。

比如下面我们这里有一个外籍球员ForeignCenter,它的调用方法和其它的类不一致,其它球员都是调用的Attack,它是用的
ForeignAttack,这样我们就没办法通过统一的接口Attack调用进攻函数,这时候就可以通过一个翻译函数Translator来将
方法ForeignAttack翻译成Attack,实现接口的统一.
具体的实现:
    先在Translator类里面定义init构造函数,在初始化时将ForeignCenter类加载进来,并赋值给self.foreignCenter
    然后定义Attack方法,该方法再调用ForeignCenter里面的ForeignAttack.
    这样我们客户端调用就只需要通过调用Translator这个类里面的Attack方法,从而实现对ForeignAttack的调用,
    这样就完成了接口的统一.
应用场景:
    比如你调用其它网站接口,返回的是xml数据,而你程序识别的是json格式数据,那么就可以弄一个适配器,来将xml的
    翻译成Json格式,这样就可以在不修改主程序的情况下,完成接口的适配
'''

def printInfo(info):
    print(info)

#球员类
class Player():
    name = ''
    def __init__(self,name):
        self.name = name

    def Attack(self,name):
        pass

    def Defense(self):
        pass

#前锋
class Forwards(Player):
    def __init__(self,name):
        Player.__init__(self,name)

    def Attack(self):
        printInfo("前锋%s 进攻" % self.name)

    def Defense(self):
        printInfo("前锋%s 防守" % self.name)

#中锋（目标类）
class Center(Player):
   def __init__(self,name):
       Player.__init__(self,name)

   def Attack(self):
       printInfo("中锋%s 进攻" % self.name)

   def Defense(self):
       printInfo("中锋%s 防守" % self.name)

#后卫
class Guards(Player):
   def __init__(self,name):
       Player.__init__(self,name)

   def Attack(self):
       printInfo("后卫%s 进攻" % self.name)

   def Defense(self):
       printInfo("后卫%s 防守" % self.name)

#外籍中锋（待适配类）
#中锋
class ForeignCenter(Player):
    name = ''
    def __init__(self,name):
        Player.__init__(self,name)

    def ForeignAttack(self):
        printInfo("外籍中锋%s 进攻" % self.name)

    def ForeignDefense(self):
        printInfo("外籍中锋%s 防守" % self.name)


#翻译（适配类）
class Translator(Player):
    foreignCenter = None
    def __init__(self,name):
        self.foreignCenter = ForeignCenter(name)

    def Attack(self):
        self.foreignCenter.ForeignAttack()

    def Defense(self):
        self.foreignCenter.ForeignDefense()


def clientUI():
    b = Forwards('巴蒂尔')
    ym = Guards('姚明')
    # 这里m就可以和上面一样调用相同的Attack()方法名,这样就保持了接口的一致.
    m = Translator('麦克格雷迪')
    # 如果没有Translator来翻译,那么下面的fm就要调用ForeignAttack,这样接口就得改动了
    fm = ForeignCenter('麦克尔杰克逊')

    b.Attack()
    m.Defense()
    ym.Attack()
    b.Defense()
    fm.ForeignAttack()
    return

if __name__ == '__main__':
    clientUI()