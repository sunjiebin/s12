#!/usr/bin/env python3
# Auther: sunjb
'''
将不同维度的产品通过桥接模式连接起来,使扩展变得更容器

'''
class AbstractRoad(object):
    '''路基类'''
    car = None

class AbstractCar(object):
    '''车辆基类'''

    def run(self):
        raise NotImplementedError

class People(AbstractRoad):
    road=None
    '''人基类'''
    def drive(self):
        print('驾驶')

class Man(People):
    def drive(self):
        print('男人驾驶')
        self.road.run()

class Woman(People):
    def drive(self):
        print('女人驾驶')
        self.road.run()
        return '女人驾驶xxx'
class Country():
    people=None
    def human(self):
        print('中国')
        res=self.people.drive()
        print('中国%s'%res)

class Street(AbstractRoad):
    '''市区街道'''

    def run(self):
        self.car.run()
        print("在市区街道上行驶")


class SpeedWay(AbstractRoad):
    '''高速公路'''

    def run(self):
        self.car.run()
        print("在高速公路上行驶")


class Car(AbstractCar):
    '''小汽车'''
    def run(self):
        print("小汽车")

class Bus(AbstractCar):
    '''公共汽车'''
    def run(self):
        print("公共汽车")


if __name__ == "__main__":
    #小汽车在高速上行驶
    road1 = SpeedWay()
    road1.car = Car()
    road1.run()

    #
    road2 = SpeedWay()
    road2.car = Bus()
    road2.run()

    road3 = Street()
    road3.car = Bus()
    road3.run()

    p1 = Man()
    p1.road = road3
    p1.drive()

    p2 = Woman()
    road4 = Street()
    road4.car = Car()
    p2.road = road4
    p2.drive()

    print('~'.center(60,'#'))
    c1 = Country()
    c1.people = p2
    c1.human()