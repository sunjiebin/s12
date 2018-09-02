#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Index,Integer,UniqueConstraint,String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

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
#先新增用户rain
fake_user = User(name='rain',password='sdfkjk')
Session.add(fake_user)
#查询rain用户存在
print(Session.query(User).filter(User.name.in_(['alex','rain'])).all())
#统计匹配的行数
print(Session.query(User).filter(User.name.in_(['alex','rain'])).count())

#回滚
Session.rollback()
#再查询rain用户消失
print(Session.query(User).filter(User.name.in_(['alex','rain'])).all())
Session.commit()
#查询并打印所有name，并且统计次数，并根据name出现的次数排序
data3=Session.query(User.name,func.count(User.name)).group_by(User.name).all()
print(data3)
#删除用户name=aa and id=6
print(Session.query(User).filter(User.name=='aa').filter(User.id==6).delete())
print(Session.query(User).all())
Session.commit()