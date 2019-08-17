from django.db import models

# Create your models here.
# 注意一定要在settings里面注册app01，否则执行makemigrations时会发现定义的建表函数都不生效
class UserType(models.Model):
    caption = models.CharField(max_length=128)
    #这里定义str函数，返回caption字段，这样别的类调用这个表的外键时，就会返回caption，而不是一个object对象了。
    def __str__(self):
        return self.caption

class UserGroup(models.Model):
    name=models.CharField(max_length=128)
    def __str__(self):
        return self.name
class UserInfo(models.Model):
    # verbose_name在ModelForm中会用到，让前端页面显示定义的名称，而非变量名。和fomm里面的llabel标签功能一样
    username=models.CharField(verbose_name='用户名',max_length=32)
    email=models.EmailField()
    user_type=models.ForeignKey(to='UserType',on_delete='CASCADE',to_field='id')
    # 注意在创建外键以及多对多关系时，对应的关系表应该写在该表的上方，如果写在该函数下方，则取不到对应关系表的函数，就会报错
    u2g=models.ManyToManyField(UserGroup)
    def __str__(self):
        return self.username
