from django.db import models

# Create your models here.

class UserGroup(models.Model):
    uid=models.AutoField(primary_key=True)
    caption=models.CharField(max_length=32,unique=True)

class UserInfo(models.Model):
    # 会创建一个名为app01_userinfo的表(注意是小写的)
    # 创建username,password列，字符串类型，长度32，64
    # 默认还会创建一个id列的主键，自增
    # 注释掉下面的行将会删除对应列，修改下面行将会对应修改列
    username=models.CharField(max_length=32,error_messages={'required':'请输入用户名'})
    password=models.CharField(max_length=128,help_text='这是一个提示信息')
    email=models.CharField(max_length=64,blank=True,verbose_name='邮箱')
    gender=models.CharField(max_length=32,default='F',editable=False)
    address=models.CharField(max_length=128,null=True)
    user_type_choice=(
        (1,'超级用户'),
        (2,'普通用户'),
        (3,'访客用户'),
    )
    # 只增加了user_type_id一列,但是在django admin里面这一列变成了下拉框,可以让用户选择上面的3中用户.
    user_type_id=models.IntegerField(choices=user_type_choice,default=1)
    # 在新版的django中,必须加上to_delete这个参数,指定删除关联表数据时此时表对应的操作,CASCADE指删除时对应表的数据也跟着删除.
    # 注意jdango默认会给外键的列名加上_id,所以这个列在数据库中名字是user_group_id,而不是user_group.
    # user_group得到的是UserGroup表的对象,通过它可以查看外键对应表里面的值,user_group_id才是外键的id
    user_group=models.ForeignKey(UserGroup,on_delete=models.CASCADE,to_field='uid',default=1)

class GroupInfo(models.Model):
    uid=models.AutoField(primary_key=True)
    caption=models.CharField(max_length=32,unique=True)
    #自动填充当前时间,允许为空.当数据插入时,填写插入时的时间
    create_time=models.DateTimeField(auto_now_add=True,null=True)
    #自动填充更新时间,当数据更新时,时间被更新
    # 这里需要注意,用update的方式更新是不生效的,需要用save()的方式更新才有效
    update_time=models.DateTimeField(auto_now=True,null=True)

class username2(models.Model):
    uid=models.AutoField(primary_key=True)
    caption=models.CharField(max_length=32)
