#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
print("生产用户文件")
user=open('user.txt','w')
user.write('sun\nluo\nzhang')
user.close()

print('生成密码文件')
passwd=open('pass.txt','w')
passwd.write('sun jiebin\nluo mi\nzhang yanhong')
passwd.close()

a=open('user.txt','r')
for i in a.readlines():
    print(i)
a.close()

b=open('pass.txt','r')
for j in b.readlines():
    print(j)
b.close()

