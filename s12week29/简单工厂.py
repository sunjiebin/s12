#!/usr/bin/env python3
# Auther: sunjb

#简单工厂模型
'''
只需要实例化一个对象，通过实例化一个对象，然后输入不同的参数，
从而实现调用不同的类
'''
class Shap(object):
    def draw(self):
        raise NotImplementedError

class Circle(Shap):
    def draw(self):
        print('circle')

class Rectangle(Shap):
    def draw(self):
        print('Rectangle')

class ShapFactory(object):
    def create(self,shap):
        if shap == 'Circle':
            return Circle()
        elif shap == 'Rectangle':
            return Rectangle()
        else:
            return None

fac=ShapFactory()
obj=fac.create('Circle')
obj.draw()
obj=fac.create('Rectangle')
obj.draw()
