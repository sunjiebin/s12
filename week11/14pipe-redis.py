#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
# !/usr/bin/env python
# -*- coding:utf-8 -*-

import redis

pool = redis.ConnectionPool(host='120.55.172.61', port=6379)

r = redis.Redis(connection_pool=pool)

# pipe = r.pipeline(transaction=False)
pipe = r.pipeline(transaction=True)

pipe.set('name', 'alex')
pipe.set('role', 'sb')

pipe.execute()