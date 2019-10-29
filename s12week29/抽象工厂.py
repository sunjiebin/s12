#!/usr/bin/env python3
# Auther: sunjb

'''
抽象工厂：
组成一整套产品的所有东西构成一个产品族
同一产品族放在同一个factory里面，一个工厂可以生产一个产品族的所有产品。
比如我需要组装一套Intel的电脑，那么就会有一套IntelFactory工厂，负责生成intel芯片组电脑的cpu/主板/内存等配件
同一类型不同品牌的产品就是同一等级结构，不同的产品类型就是不同的产品等级结构，比如AMD和Intel的cpu就为同一等级结构。
所以，一个产品族里面有着不同的产品等级结构
下面的函数抽象了

生成抽象工厂AbstractFactory，再定义好具体实现的工厂IntelFactory，工厂里面定义了生成产品的方法createCpu，createMainboard，
工厂类并不直接生成产品，而是通过相应的create方法调用对应的产品类，再由产品类去实际生产需要的产品。
生成抽象产品AbstractCpu，再定义好具体的产品IntelCpu，继承抽象产品，这个类被工厂调用
生成组装工程师ComputerEngineer，利用工程师调用不同的工厂，再触发工厂里面的create函数来生成不同的产品。
主装类负责将需要生成的配件一一生成，并组装成一个整体返回给客户。

客户只需要知道要采用那个芯片家族的产品，然后交给组装工程师去实现即可。不需要关心这台电脑到底需要哪些配件，各个配件需要什么型号。
所以客户调用就只需要实例化ComputerEngineer和IntelFactory即可。并将IntelFactory传给ComputerEngineer

抽象工厂的优点：
    1.分离了接口的实现。客户端不需要知道Intel的机器具体需要哪些配件，也不需要知道配件直接的依赖关系。
        这个和工厂方法有着本质的区别，工厂方法需要自己生成产品并去组装，不同产品线的依赖也需要客户端自己解决。
        比如老男孩上海的课程被用在了北京分校，这个也会被允许。但是这个在抽象工厂里面不会出现，因为组件已经在工厂
        里面封装好了，不需要客户自己来定义了组装。
    2.是产品切换变得更容易,django里面支持各种数据库的连接,这很可能也是一种抽象工厂模式.
缺点：
    1.扩展不容易，如果需要新加产品就得修改工厂代码.

'''
class AbstractFactory(object):
    computer_name = ''
    def createCpu(self):
        pass
    def createMainboard(self):
        pass

class InterFactory(AbstractFactory):
    computer_name = 'Intel I7 computer'
    def createCpu(self):
        return IntelCpu('i7-8500')
    def createMainboard(self):
        return IntelMainBoard('intel-6000')

class AmdFactory(AbstractFactory):
    computer_name = 'Amd 4 computer '

    def createCpu(self):
        return AmdCpu('amd444')

    def createMainboard(self):
        return AmdMainBoard('AMD-4000')

class AbstractCpu(object):
    series_name = ''
    instructions = ''
    arch=''

class IntelCpu(AbstractCpu):
    def __init__(self,series):
        self.series_name = series

class AmdCpu(AbstractCpu):
    def __init__(self,series):
        self.series_name = series

class AbstractMainboard(object):
    series_name = ''

class IntelMainBoard(AbstractMainboard):
    def __init__(self,series):
        self.series_name = series

class AmdMainBoard(AbstractMainboard):
    def __init__(self,series):
        self.series_name = series

class ComputerEngineer(object):
    def makecomputer(self,factory_obj):
        self.prepareHardware(factory_obj)
    def prepareHardware(self,factory_obj):
        self.cpu=factory_obj.createCpu()
        self.mainboard=factory_obj.createMainboard()
        info = '''------- computer [%s] info:
           cpu: %s
           mainboard: %s

        -------- End --------
               ''' % (factory_obj.computer_name, self.cpu.series_name, self.mainboard.series_name)
        print(info)

if __name__ == '__main__':
    engineer=ComputerEngineer()
    intel_factory=InterFactory()
    engineer.makecomputer(intel_factory)

    amd_factory=AmdFactory()
    engineer.makecomputer(amd_factory)
