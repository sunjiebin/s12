from django.db import models

# Create your models here.
class Department(models.Model):
    # 没有定义AutoField自增列，所以会自动添加id列
    fullname = models.CharField(max_length=32)
    code = models.CharField(max_length=32,null=True)

class Host(models.Model):
    # 定义了nid自增列，所以不再自动添加id列
    nid = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=32,db_index=True)
    ip = models.GenericIPAddressField(protocol='ipv4',db_index=True)
    port = models.IntegerField()
    to_department = models.ForeignKey(on_delete='CASCADE',to=Department)

# ManyToManyField('Host)会自动创建一张关系表myapp_applications_r,这张表会将applications和host表的主键自动关联。列名applications_id，host_id
class Applications(models.Model):
    name = models.CharField(max_length=128)
    r = models.ManyToManyField('Host')
