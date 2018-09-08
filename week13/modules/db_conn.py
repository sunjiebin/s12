#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conf import settings

engine=create_engine(settings.ConnParams)
SessionCls=sessionmaker(bind=engine)
session=SessionCls()
