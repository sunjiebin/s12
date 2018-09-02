#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from s12.week12 import orm_create_table14
from sqlalchemy.orm import sessionmaker

Session_class=sessionmaker(bind=orm_create_table14.engine)  #创建与数据库会话的session，其中engin是从orm_fk14模块中导入而来
session=Session_class()     #实例化session

addr1=orm_create_table14.Address(street='minzhi', city='longhua', state='gd')
addr2=orm_create_table14.Address(street='haiancheng', city='nanshan', state='gd')
addr3=orm_create_table14.Address(street='dameisha', city='yantian', state='gd')
addr4=orm_create_table14.Address(street='changzhen', city='gongming', state='gd')
session.add_all([addr1,addr2,addr3,addr4])
c1=orm_create_table14.Customer(name='alex', billing_address=addr1, shipping_address=addr2)
c2=orm_create_table14.Customer(name='jack', billing_address=addr2, shipping_address=addr2)
session.add_all([c1,c2])
session.commit()