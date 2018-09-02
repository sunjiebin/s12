#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from s12.week12 import book_table15
from sqlalchemy.orm import sessionmaker
Sessio_class=sessionmaker(bind=book_table15.engine)
session=Sessio_class()
#通过作者名称查找其出版的书籍
author_obj=session.query(book_table15.Author).filter(book_table15.Author.name=='Alex').first()
print(author_obj.Books)
#查找书籍对应的作者
book_obj=session.query(book_table15.Book).filter(book_table15.Book.name=='learn ansible').first()
print(book_obj.authors)