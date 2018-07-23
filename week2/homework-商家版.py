#!/usr/bin/env python
# Python version: python3
# Auther: sunjb

import shelve,os
biz_dbfile='goods.txt'


'''导入老的商品'''
if os.path.isfile(biz_dbfile+'.dat'):
    dbwrite = shelve.open(biz_dbfile)
    goodslist_old=dbwrite.get('goodslist')
    print(goodslist_old)
else:
    print('第一次运行，将创建数据文件')
    dbwrite = shelve.open(biz_dbfile)
    goodslist_old={}

choice=input('''商家版，请选择：
1、修改或新增商品
2、删除商品''')

goodslist_new={}

if choice.isdigit() and int(choice)==1:
    '''添加商品'''
    print(choice)
    while True:
        goods=input('请输入商品名称：').strip()
        cost=input('请输入商品价格：')
        if cost.isdigit():
            cost=int(cost)
            goodslist_new[goods]=cost


        else:
            print('商品价格必需是数字，请重新输入')
            continue

        #继续添加商品选择
        addchoice=input('是否继续添加商品y/n：')
        if addchoice == 'y' or addchoice=='':
            continue
        else:
            print(goodslist_new)
            dbchoice=input('''以上是您新增的商品列表，是否保存y/n''')
            if dbchoice == 'y' or dbchoice == '':
                goodslist=dict(goodslist_old,**goodslist_new)
                dbwrite['goodslist']=goodslist
                print('已经保存')
            else:
                print('本次修改不会被保存')
            exit()
elif choice.isdigit() and int(choice)==2:
    '''下线商品'''
    while True:
        goods=input('请输入商品名称：').strip()
        try:
            goodslist_old[goods]
            goodslist_old.pop(goods)
            print(goods)
        except:
            print('您输入的商品名称不存在，请重新输入')
else:
    print('输入不正确，请重新输入')
