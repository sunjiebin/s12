#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
'''
sqlalchemy底层会调用pymysql来完成封装，这里要指定mysql+pymysql代表底层调用pymysql
echo=True会把所有的执行过程打印出来，如果不加就不会打印执行过程
'''
engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/sun", encoding='utf-8',echo=True,max_overflow=5)

Base = declarative_base()       #生成基类


# 创建单表
class Users(Base):
    __tablename__ = 'users'     #表名
    id = Column(Integer, primary_key=True)  #Column,Interger都是通过上面import导入的
    name = Column(String(32))
    password = Column(String(16))

    __table_args__ = (
        UniqueConstraint('id', 'name', name='uix_id_name'),
        Index('ix_id_name', 'name', 'extra'),
    )

'''上面的操作只是定义了创建表，并不会执行创建表，下面的语句才是调用engin连上mysql执行创建操作
通过下面的Base操作，会把所有继承了它的类都执行，如上面的Users(Base)类就会被执行
'''
Base.metadata.create_all(engine)  #创建表结构，如果已经存在，则不创建

#创建数据
'''生成一个类，创建与数据库会话的session类，这是类不是实例'''
Session_class=sessionmaker(bind=engine)
Session=Session_class() #对类实例化,相当于pymysql里面的cursor
user_obj=Users(name='alex',password='alex123')  #生成要创建的数据对象
user_obj2=Users(name='sun',password='223344')
print(user_obj.name,user_obj.id)    #此时对象还未创建，所以id还不存在，打印不Null
Session.add(user_obj,user_obj2)   #把要创建的数据对象添加到session里面，一会统一创建
Session.commit()    #提交执行结果，此时数据才被真正的创建
print(user_obj.name,user_obj.id)