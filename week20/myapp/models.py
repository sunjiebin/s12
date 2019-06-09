from django.db import models

# Create your models here.

class Bussiness(models.Model):
    # 没有定义AutoField自增列，所以会自动添加id列
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32,null=True)

class Host(models.Model):
    # 定义了nid自增列，所以不再自动添加id列
    nid = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=32,db_index=True)
    ip = models.GenericIPAddressField(protocol='ipv4',db_index=True)
    port = models.IntegerField()
    # 注意，由于是ForeignKey，所以在数据库里面列名会变为b_id，而不是b。这时候b代表的是Bussiness对象，可以用b.code来获取Bussiness里面的code列数据
    b = models.ForeignKey(on_delete='CASCADE',to=Bussiness,to_field='id')