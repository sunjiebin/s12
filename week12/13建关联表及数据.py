#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Index,Integer,UniqueConstraint,String,DATE,Enum,ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship

engine=create_engine("mysql+pymysql://root:sunjiebin@localhost:3306/sun",encoding='utf-8',max_overflow=5)
Base=declarative_base()

class Student(Base):
    __tablename__ = 'student'     #表名
    '''注意：下面建表语句中的Interger,String,DATA等列的类型都要在上面import导入，否则会报错
    '''
    id = Column(Integer, primary_key=True,autoincrement=True)  #Column,Interger都是通过上面import导入的
    name = Column(String(32),nullable=False)
    regester_date = Column(DATE,nullable=False)
    gender=Column(Enum("M","F"),nullable=False)

    __table_args__ = (
        Index('ix_id_name', 'name'),
    )

    def __repr__(self):
        return "<%s name: %s>" %(self.id,self.name)

class StudentRecord(Base):
    __tablename__='student_record'
    id = Column(Integer, primary_key=True, autoincrement=True)
    day=Column(Integer,nullable=False)
    status=Column(String(32),nullable=False)
    stu_id=Column(Integer,ForeignKey('student.id'))
    student=relationship('Student',backref='my_student_record')
    def __repr__(self):
        return "<%s name: %s>" %(self.id,self.day)

Base.metadata.create_all(engine)
Session_class=sessionmaker(bind=engine)
Session=Session_class()

s1=Student(name='s1',regester_date='2018-08-29',gender='M')
Session.add(s1)
Session.add_all([
    Student(name='s2',regester_date='2018-08-29',gender='M'),
    Student(name='sun', regester_date='2018-08-29', gender='M'),
    Student(name='luo', regester_date='2018-08-28', gender='F'),
    Student(name='jie', regester_date='2018-08-28', gender='F'),
    StudentRecord(day=1,status='Y',stu_id=1),
    StudentRecord(day=2,status='N',stu_id=1),
    StudentRecord(day=3,status='Y',stu_id=1),
    StudentRecord(day=1,status='Y',stu_id=2)
])
Session.commit()