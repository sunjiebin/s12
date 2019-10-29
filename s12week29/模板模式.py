#!/usr/bin/env python3
# Auther: sunjb

'''
比如用户认证可以通过qq，也可以通过微信，这两个的流程是相同的，
都是先注册，然后登录，最后实现认证。
那么，可以写一个基类，包含了注册/登录/认证。
再写一个qq/微信的类，继承基类，并重写基类的注册/登录的方法，
来实现注册和登录的差异化。
然后都统一调用基类的auth方法实现认证。

'''
class Register(object):
    '''用户注册接口'''

    def register(self):
        pass
    def login(self):
        pass

    def auth(self):
        self.register()
        self.login()

class RegisterByQQ(Register):
    '''qq注册'''

    def register(self):
        print("---用qq注册-----")

    def login(self):
        print('----用qq登录-----')



class RegisterByWeiChat(Register):
    '''微信注册'''

    def register(self):
        print("---用微信注册-----")

    def login(self):
        print('----用微信登录-----')


if __name__ == "__main__":

    register1 = RegisterByQQ()
    register1.auth()

    register2 = RegisterByWeiChat()
    register2.auth()