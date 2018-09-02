#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
from s12.week12 import book_table15
from sqlalchemy.orm import sessionmaker
Sessio_class=sessionmaker(bind=book_table15.engine)
session=Sessio_class()

author_obj=session.query(book_table15.Author).filter(book_table15.Author.name=='Alex').first()
print(author_obj)
book_obj=session.query(book_table15.Book).filter(book_table15.Book.id==2).first()
print(book_obj.authors)
book_obj.authors.remove(author_obj)
print(book_obj.authors)
session.commit()