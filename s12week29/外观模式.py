#!/usr/bin/env python3
# Auther: sunjb

#外观模式（Facade），为子系统中的一组接口提供一个一致的界面，定义一个高层接口，这个接口使得这一子系统更加容易使用。
# 在以下情况下可以考虑使用外观模式：
# (1) 设计初期阶段，应该有意识的将不同层分离，层与层之间建立外观模式。
# (2) 开发阶段，子系统越来越复杂，增加外观模式提供一个简单的调用接口。
# (3) 维护一个大型遗留系统的时候，可能这个系统已经非常难以维护和扩展，但又包含非常重要的功能，为其开发一个外观类，以便新系统与其交互。

# 优点编辑
# （1）实现了子系统与客户端之间的松耦合关系。
# （2）客户端屏蔽了子系统组件，减少了客户端所需处理的对象数目，并使得子系统使用起来更加容易。

'''
就比如下面的基金买卖,每次买卖基金我需要买入股票/国债/权证等各类指数,那么此时,如果我一个个的类实例化和调用,
那会显得相当的麻烦.而且用户还需要记得有哪些类需要一个个实例化,以及其调用的方式.
这时候就可以加一层Fund类,通过这个类完成对上面所有操作的实例化和调用,这样客户端
就只需要调用这一个类就好了.简化了客户端的操作.

'''

def printInfo(info):
    print(info)

class Stock():
    name = '股票'
    def buy(self):
        printInfo('买 '+self.name)

    def sell(self):
        printInfo('卖 '+self.name)

class ETF():
    name = '指数型基金'
    def buy(self):
        printInfo('买 '+self.name)

    def sell(self):
        printInfo('卖 '+self.name)

class Future():
    name = '期货'
    def buy(self):
        printInfo('买 '+self.name)

    def sell(self):
        printInfo('卖 '+self.name)

class NationDebt():
    name = '国债'
    def buy(self):
        printInfo('买 '+self.name)

    def sell(self):
        printInfo('卖 '+self.name)

class Option():
    name = '权证'
    def buy(self):
        printInfo('买 '+self.name)

    def sell(self):
        printInfo('卖 '+self.name)

#基金
class Fund():

    def __init__(self):
        self.stock = Stock()
        self.etf = ETF()
        self.future = Future()
        self.debt = NationDebt()
        self.option = Option()

    def buyFund(self):
        self.stock.buy()
        self.etf.buy()
        self.debt.buy()
        self.future.buy()
        self.option.buy()

    def sellFund(self):
        self.stock.sell()
        self.etf.sell()
        self.future.sell()
        self.debt.sell()
        self.option.sell()

def clientUI():
    myFund = Fund()
    myFund.buyFund()
    myFund.sellFund()
   # return


if __name__ == '__main__':
    clientUI()