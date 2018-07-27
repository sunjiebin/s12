#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

class people():
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def eat(self):
        print('%s is eating...'%(self.name))

    def drink(self):
        print('%s is drinking....'%(self.name))
class man(people):
