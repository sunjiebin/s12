#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Index,Integer,UniqueConstraint,String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine("mysql+pymysql://root:sunjiebin@localhost:3306/sun",encoding='utf-8',max_overflow=5)
Base=declarative_base()

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

Session_class=sessionmaker(bind=engine)
Session=Session_class()
#查询
#查询name为alex的行，all()代表所有行，first()代表只查一行
data=Session.query(User).filter_by(name='alex').first()
#查询id>2 and id<4的,注意这里是filter，不是filter_by
data2=Session.query(User).filter(User.id>2).filter(User.id<4).all()
print(data)
print(data2)

#将前面查出的值修改
data.name='mi'
data.password='gaga'
Session.commit()

