#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

a=open('file.txt','r')
for i in range(3):
    name_input=input('input your name:')
    for i in a.readlines():
        name=i.split('=')[0]
        pwd=i.split('=')[1]
        a.seek(0)
        if name_input.strip() == name:
            print('用户名正确!')
            for j in range(3):
                # 判断用户锁文件，0正常，1锁定
                if lock == '0':
                    n = 2 - j
                    pwd_input = input('input your password:')
                    # 判断密码是否正确
                    if pwd_input == pwd:
                        print('登陆成功')
                        break
                    else:
                        print('密码不正确,你还可以尝试%d次' % n)
                    # 判断密码错误次数，3次后会修改锁文件值为1
                    if n == 0:
                        print('你尝试太多次，用户被锁定')
                        lock = open('lock.txt', 'w')
                        lock.write('1')
                        lock.close()
                else:
                    print('用户已经被锁定')
                    break
            break
        print('用户名不正确，请重新输入')
        if i == 2:
            print('尝试太多次了，退出脚本')
a.close()