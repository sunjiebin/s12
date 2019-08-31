from django.db import models
from bbs.models import UserProfile
# Create your models here.

class WebGroup(models.Model):
    name=models.CharField(max_length=32,verbose_name='群名称')
    brief=models.CharField('群介绍',max_length=255,blank=True,null=True)
    owner=models.ForeignKey(UserProfile,verbose_name='群主',on_delete=models.CASCADE,max_length=32)
    admins=models.ManyToManyField(UserProfile,related_name='group_admins',blank=True,verbose_name='管理员')
    members=models.ManyToManyField(UserProfile,related_name='group_members',blank=True,verbose_name='成员')
    max_members=models.IntegerField(default=200)

    def __str__(self):
        return self.name