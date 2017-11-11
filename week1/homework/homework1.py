#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
'''要求：
1、输入用户名和密码
2、认证成功后显示欢迎信息
3、输错三次后锁定'''
'''
脚本流程
1、判断用户名是否正确，如果不正确则返回用户名不正确，如此循环三次，三次后退出脚本
2、如果用户名正确，则判断用户是否被锁，如果被锁则退出脚本
3、如果用户没被锁，则让用户输入密码，密码3次错误则锁定用户，输入正确则提示登录成功。
'''

#打开用户名和密码表
a=open('userpass.txt','r')
#设置默认标签值
flag='false'
flag2='in'
flag3='in'

#用户名尝试3次错误退出
for num in range(3):
    name_input=input('input your name:')
    for i in a.readlines():
        name=i.split('=')[0]
        #注意：一定要加上strip去掉换行符，因为默认会把换行符给带到变量里面，导致变量多了一个换行会，sunjb和”sunjb+换行符“是不相等的
        pwd=i.split('=')[1].strip('\n')
        a.seek(0)
        #判断用户名是否正确，正确后进入下一步循环
        if name_input.strip() == name:
                #读取锁文件，判断用户是否在锁文件内，如果存在则退出脚本
                lockfile=open('lock.txt','r')
                for lockuser in lockfile.readlines():
                    if name_input.strip() == lockuser.strip():
                        print('用户已经被锁定')
                        flag2='out'
                        break
                    lockfile.seek(0)
                lockfile.close()
                if flag2 == 'out':
                    flag3='out'
                    break
                #进入密码判断循环
                print('用户名正确!')
                for j in range(3):
                    #判断用户锁文件，0正常，1锁定
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
                            lock=open('lock.txt','a')
                            lock.write(name_input+'\n')
                            lock.close()
                flag='true'
                break
    if flag3 == 'out':
        break
    #第三次输错用户名会退出脚本
    if num == 2:
        print('尝试太多次了，退出脚本')
        break
    #当用户名不匹配时提示
    if flag == 'false':
        print('用户名不正确，请重新输入')
    else:
            break

a.close()

