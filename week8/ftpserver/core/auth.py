#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
import sys,json

class UserConf(object):

    def __init__(self,user,passwd):
        self.user=user
        self.passwd=passwd

    def user_quota(self):
        pass

    def user_auth(self):
        pass

    def user_home(self):
        pass

user=sys.argv[1]
passwd=sys.argv[2]
fun=UserConf(user,passwd)
