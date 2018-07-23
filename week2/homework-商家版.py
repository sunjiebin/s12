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
    if goodslist_old is None:
        print('数据文件已存在，但列表为空')
        goodslist_old={}
else:
    print('第一次运行，将创建数据文件')
    dbwrite = shelve.open(biz_dbfile)
    goodslist_old={}

choice=input('''请选择：
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
            print('已经选择添加的商品有%s'%goodslist_new)
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
    dellist=[]
    while True:
        goods=input('请输入商品名称：').strip()
        print(goodslist_old.get(goods))
        if  goodslist_old.get(goods):
            goodslist_old.pop(goods)
            dellist.append(goods)
            print('本次删除的产品为%s'%goods)
            delchoice=input('是否继续删除其它商品y/n，默认是y')
            if delchoice == 'y' or delchoice == '':
                print('当前产品还有%s'%goodslist_old)
                print('待删除的产品为%s'%dellist)
                continue
            else:
                print('待删除的产品为%s' % dellist)
                affirm=input('是否确认删除y/n，默认是y')
                if affirm == 'y' or affirm == '':
                    print(goodslist_old)
                    dbwrite['goodslist']=goodslist_old
                    print('商品已经被下架')
                    exit()
                else:
                    print('本次将不会下架任何商品')
                    exit()
        else:
            print('您输入的商品名称不存在，请重新输入')
else:
    print('输入不正确，请重新输入')
