#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

import pymysql
#创建连接
conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='sunjiebin',db='sun')
#创建游标
cursor=conn.cursor()
#执行sql,并返回影响行数
effect_rot=cursor.execute("update hosts set host='1.1.1.2'")
# 执行SQL，并返回受影响行数
# effect_row = cursor.execute("update hosts set host = '1.1.1.2' where nid > %s", (1,))
# 执行SQL，并返回受影响行数
# effect_row = cursor.executemany("insert into hosts(host,color_id)values(%s,%s)", [("1.1.1.11",1),("1.1.1.11",2)])

#同时插入两条数据
cursor.executemany("insert into hosts(host,color_id)values(%s,%s)", [("1.1.1.11",1),("1.1.1.11",2)])
# 提交，不然无法保存新建或者修改的数据
conn.commit()

#查询数据
cursor.execute("select * from hosts")
'''
在fetch数据时按照顺序进行，可以使用cursor.scroll(num,mode)来移动游标位置，如：
cursor.scroll(1,mode='relative')  # 相对当前位置移动
cursor.scroll(2,mode='absolute') # 相对绝对位置移动
'''
# 获取第一行数据
row_1 = cursor.fetchone()

# 获取前n行数据
# row_2 = cursor.fetchmany(3)
# 获取所有数据
#row_3 = cursor.fetchall()

# 关闭游标
cursor.close()
# 关闭连接
conn.close()