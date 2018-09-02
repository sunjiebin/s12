#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from s12.week12 import book_table15
from sqlalchemy.orm import sessionmaker

b1=book_table15.Book(name='learn python',pub_date='2018-08-31')
b2=book_table15.Book(name='learn ansible',pub_date='2018-09-01')
b3=book_table15.Book(name='learn english',pub_date='2019-03-08')

a1=book_table15.Author(name='Alex')
a2=book_table15.Author(name='sun')
a3=book_table15.Author(name='mi')

b1.authors=[a1,a2]
b2.authors=[a1,a2,a3]

Sessio_class=sessionmaker(bind=book_table15.engine)
session=Sessio_class()
session.add_all([
    b1,b2,b3,a1,a2,a3
])
session.commit()