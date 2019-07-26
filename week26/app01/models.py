from django.db import models

# Create your models here.

class UserInfo(models.Model):
    name=models.CharField(max_length=32)
    age=models.IntegerField()

class BussinessUnit(models.Model):
    name=models.CharField(max_length=32)

class Server(models.Model):
    server_type_choice=(
        (1,'存储'),
        (2,'web'),
        (3,'缓存'),
    )
    server_type=models.IntegerField(choices=server_type_choice,default=None)
    hostname=models.CharField(max_length=64)
    port=models.IntegerField()
    bussiness_unit=models.ForeignKey(BussinessUnit,on_delete=models.CASCADE)
    user=models.ForeignKey(UserInfo,on_delete=models.SET_DEFAULT,default=1)