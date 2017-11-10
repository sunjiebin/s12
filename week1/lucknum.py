#!/usr/bin/env python
# --- coding:utf-8 ----
print ('这是一个猜数字的游戏')
luck=16
guess_number=0
while guess_number<3:
    guess_number+=1
    print('尝试%s次数'%(guess_number))
    num = int(input('please input your number:'))

    if num < luck:
        print ('再大一点吧！')
    elif num > luck:
        print ('太大了吧！')
    else:
        print ('wow,你猜对了，太棒了！')
        break
else:
    print ('猜测次数已到！')