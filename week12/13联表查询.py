#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Index,Integer,UniqueConstraint,String,DATE,Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine("mysql+pymysql://root:sunjiebin@localhost:3306/sun",encoding='utf-8',max_overflow=5)
Base=declarative_base()

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True,autoincrement=True)  #Column,Interger都是通过上面import导入的
    name = Column(String(32),nullable=False)
    regester_date = Column(DATE,nullable=False)
    gender=Column(Enum("M","F"),nullable=False)
    def __repr__(self):
        return "<id:%s name:%s date:%s>" %(self.id,self.name,self.regester_date)

class User(Base):
    __tablename__ = 'users'     #表名
    id = Column(Integer, primary_key=True)  #Column,Interger都是通过上面import导入的
    name = Column(String(32))
    password = Column(String(16))

    __table_args__ = (
        UniqueConstraint('id', 'name', name='uix_id_name'),
        Index('ix_id_name', 'name'),
    )

    def __repr__(self):
        return "<%s name: %s>" %(self.id,self.name)

#Base.metadata.create_all(engine)
Session_class=sessionmaker(bind=engine)
Session=Session_class()
#联表，查找两个表中name相等的
print(Session.query(Student,User).filter(Student.name==User.name).all())
#如果定义了外键，可以用下面这个方式去查
#print(Session.query(User).join(Student).all())