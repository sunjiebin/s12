#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
import sys
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
