#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
import sys,json,os,hashlib

class UserConf(object):
    '''用户认证模块'''
    def __init__(self, login_user, login_passwd):
        self.login_user=login_user
        self.login_passwd=login_passwd
        self.__readconf()

    def __readconf(self):
        basepath = os.path.dirname(os.path.dirname(filename))
        conf = os.path.join(basepath, 'conf/user.conf')
        f = open(conf, 'r')
        self.data = json.load(f)
        print(self.data)
        f.close()

    def user_quota(self):
        pass

    def user_auth(self):

        user_data=self.data.get(self.login_user)
        print(user_data)
        if user_data:
            user_pass=user_data.get('passwd')
            if self.login_passwd == user_pass:
                print('%s登录成功!'%self.login_user)
            else:
                print('用户%s密码不正确'%self.login_user)
        else:
            print('%s用户不存在'%self.login_user)
    def user_home(self):
        pass

filename=sys.argv[0]
login_user=sys.argv[1]
login_passwd=sys.argv[2]
fun=UserConf(login_user,login_passwd)
fun.user_auth()