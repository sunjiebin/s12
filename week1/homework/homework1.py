#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''要求：
1、输入用户名和密码
2、认证成功后显示欢迎信息
3、输错三次后锁定'''

#截取文件里面的用户名
file=open('userpass.txt','r')
name=file.readline().split('=')[0]
#截取文件里面的密码
file.seek(0)
pwd=file.readline().split('=')[1]

#获取锁文件的值
lockfile=open('lock.txt','r')
lock=lockfile.read()
lockfile.close()

#用户名尝试3次错误退出
for i in range(3):
    name_input=input('input your name:')
    #判断用户名是否正确，正确后进入下一步循环
    if name_input.strip() == name:
        print('用户名正确!')
        #进入密码判断循环
        for j in range(3):
            #判断用户锁文件，0正常，1锁定
            if lock=='0':
                n=2-j
                pwd_input = input('input your password:')
                #判断密码是否正确
                if pwd_input == pwd:
                    print('登陆成功')
                    break
                else:
                    print('密码不正确,你还可以尝试%d次'%n)
                #判断密码错误次数，3次后会修改锁文件值为1
                if n == 0:
                    print('你尝试太多次，用户被锁定')
                    lock=open('lock.txt','w')
                    lock.write('1')
                    lock.close()
            else:
                print('用户已经被锁定')
                break
        break
    print('用户名不正确，请重新输入')
    if i == 2:
        print('尝试太多次了，退出脚本')
file.close()

