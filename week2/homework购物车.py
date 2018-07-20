#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
import sys

list=[('iphone',5800),('mac',12000),('bike',800),('starbuck',38),('p10',5200)]
yourlist=[]
salary=input('请告诉我你有多少钱')
if salary.isdigit():
   salary=int(salary)
   while True:
       print('以下是可购买的商品列表'.center(50,'#'))
       for i,j in enumerate(list):
           print(i,j)
       choice=input('请输入你要购买的商品编号')
       if choice.isdigit():
           choice=int(choice)
           if choice>=0 and choice<len(list):
               goods=list[choice][0]
               price=list[choice][1]
               if salary>=price:
                   salary = salary - price
                   yourlist.append(list[choice])
                   print('你购买的商品为\n%s'%yourlist)
                   print('你的钱还剩余:\033[31;1m%s\033[0m'%salary)
               else:
                   print('你购买的商品为\n%s'%yourlist)
                   print('你的钱还剩余:\033[31;1m%s\033[0m'%(salary))
                   print('你的钱不够啦，请结账')
                   exit()
           else:
               print('你输入的商品不存在，请重新输入')
       elif choice is 'q':
           print('你购买的商品为%s' % yourlist)
           print('你的钱还剩余\033[31;1m%s\033[0m' % salary)
           exit(0)
       else:
           print('你输入的不正确，请重新输入')
else:
    print('请输入数字')

'''
try:
    yourmoney=int(input('请告诉我你有多少钱'))
    print(type(yourmoney))
except:
    print('请输入整数数字')


list={
    1:['iphone',5800],
    2:['mac',12000],
    3:['starbuck',38],
    4:['bike',800]
}

yourgoods=[]

while True:
        print(list)
        choice=input('你要买买买吗y/n')
        if choice == 'n':
            print('你购买的商品为%s,余额为%s'%(yourgoods,yourmoney))
            break
        else:
            num = int(input('请选择你要的商品编号'))
            goods = list.get(num)[0]
            price = list.get(num)[1]
            yourmoney = yourmoney - price
            if yourmoney < 0:
                print('你都没钱了还买个屁,赶紧结账滚')
                break
            else:
                print('您当前余额还有:%s'%(yourmoney))
                yourgoods.append(goods)
                print('您当前已选商品为%s'%(yourgoods))
                continue
'''