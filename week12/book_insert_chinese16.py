#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Index,Integer,UniqueConstraint,String,DATE,Enum,ForeignKey,Table
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
'''注意，教程中说到如果要插入中文，需要在库名后加上?charset=utf8，不然会报错
但在我这里就算没加这个字符串，也并没有报错，可能与我mysql8默认采用utf8mb4有关'''
engine=create_engine("mysql+pymysql://root:sunjiebin@localhost:3306/sun",encoding='utf-8',max_overflow=5)
#所以如果在其它环境插入中文报错，可用下面的写法,其中encoding='utf-8'这个可以去掉不影响
#engine=create_engine("mysql+pymysql://root:sunjiebin@localhost:3306/sun?charset=utf8",encoding='utf-8',max_overflow=5)

Base=declarative_base()
'''如果确认不会对建的表有处理操作，那么建表语句也可以像下面这样简写'''
book_m2m_author = Table('book_m2m_author',Base.metadata,
                        Column('book_id',Integer,ForeignKey('books.id')),
                        Column('author_id',Integer,ForeignKey('authors.id')),
                        )
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)  #Column,Interger都是通过上面import导入的
    name = Column(String(32),nullable=False)
    pub_date=Column(DATE)
    authors=relationship('Author',secondary=book_m2m_author,backref='Books')
    def __repr__(self):
        return self.name

class Author(Base):
    __tablename__='authors'
    id=Column(Integer,primary_key=True)
    name=Column(String(32))
    def __repr__(self):
        return self.name

Base.metadata.create_all(engine)

#插入
Session_class=sessionmaker(bind=engine)
session=Session_class()

b4=Book(name='跟老孙去西天',pub_date='2088-09-09')
session.add(b4)
session.commit()
