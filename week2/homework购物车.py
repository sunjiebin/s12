#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
import sys,shelve,os,collections

#list=[('iphone',5800),('mac',12000),('bike',800),('starbuck',38),('p10',5200)]
biz_dbfile='goods.txt'
user_dbfile='userdb.txt'
dbread=shelve.open(biz_dbfile)
userwrite=shelve.open(user_dbfile)

'''判断商家数据'''
if os.path.isfile(biz_dbfile+'.dat'):
    dbwrite = shelve.open(biz_dbfile)
    goodslist=dbwrite.get('goodslist')
    list=list(goodslist.items())
    #print(list)

    if goodslist is None:
        print('还未上线任何商品')
        goodslist={}
else:
    print('本店还未开业')
    exit(1)

'''判断用户数据'''
if not os.path.isfile(user_dbfile+'.dat'):
    print('欢迎首次光临本店')
    salary = input('请告诉我你有多少钱')
    userlist=[]
    if not salary.isdigit():
        print('请输入数字')
        exit()
    salary = int(salary)

else:
    salary = userwrite.get('userprice')
    userlist=userwrite.get('userlist')
    oldlist = collections.Counter(userlist)
    print('之前购买的商品列表', oldlist)
    print('用户余额',salary)

yourlist=[]



while True:
   print('以下是可购买的商品列表'.center(50,'#'))
   for i,j in enumerate(list):
       print(i,j)
   choice=input('请输入你要购买的商品编号，结束请按q')
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
       confirm=input('是否确认购买？y/n')
       if confirm == 'y' or confirm == '':
           userlist.extend(yourlist)
           userprice=salary
           userwrite['userlist']=userlist
           userwrite['userprice']=userprice
           print('商品信息及余额已保存')
           exit(0)
       else:
           print('本次购买不会生效')
   else:
       print('你输入的不正确，请重新输入')

