#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
from s12.week12 import orm_create_table14
from sqlalchemy.orm import sessionmaker

Session_class=sessionmaker(bind=orm_create_table14.engine)  #创建与数据库会话的session，其中engin是从orm_fk14模块中导入而来
session=Session_class()     #实例化session

obj=session.query(orm_create_table14.Customer).filter(orm_create_table14.Customer.name=='alex').first()
#obj=session.query(orm_create_table14.Customer).filter(orm_create_table14.Customer.name=='alex').all()
#如果上面用all()，则用print(obj)
#print(obj)
'''注意上面如果用all()的写法，则不支持下面的obj.name操作，因为用all时返回的是一个List列表类型，这个类型
不支持用obj.name的操作， 用first()可以，因为它返回的是class类，可以obj.name操作'''
print(type(obj))
print(obj.name,obj.billing_address)