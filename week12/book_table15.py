#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Index,Integer,UniqueConstraint,String,DATE,Enum,ForeignKey,Table
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

engine=create_engine("mysql+pymysql://root:sunjiebin@localhost:3306/sun",encoding='utf-8',max_overflow=5)
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
    '''关联Author函数，也就是和里面的authors表进行关联，两者通过book_m2m_author中的外键来建立两个表的关联，
    注意这里的secondary后面接的是Table后面的表名，而不是=号前面的实例名，Author回调时用Books可关联到Book'''
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