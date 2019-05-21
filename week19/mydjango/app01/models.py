from django.db import models

# Create your models here.

class UserInfo(models.Model):
    # 会创建一个名为app01_userinfo的表(注意是小写的)
    # 创建username,password列，字符串类型，长度32，64
    # 默认还会创建一个id列的主键，自增
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=64 )