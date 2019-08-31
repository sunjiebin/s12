from django.db import models
#引用django自带的用户
from django.contrib.auth.models import User
import datetime
#这个方法用于在操作不符合条件时，在页面上出现红色的错误提示。
from django.core.exceptions import ValidationError

# Create your models here.

#参考：https://docs.djangoproject.com/en/2.1/ref/models/fields/#field-types


class Article(models.Model):
    # 默认第一个字段就是verbose_name，如果不写，默认将用变量名称作为该名称
    title=models.CharField('文章标题',max_length=255)
    brief=models.CharField(null=True,blank=True,max_length=255,verbose_name='文章简介') #null=True只是用于在数据库中存储空值，并不用于校验
    category=models.ForeignKey('Category',on_delete=models.CASCADE)
    content=models.TextField(u'文章内容')
    author=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    pub_date=models.DateTimeField('发布时间',blank=True,null=True)                     #这里不能创建的时候就填时间，因为有时候是草稿，这时候不能把草稿当作发布时间
    last_modify=models.DateTimeField(auto_now=True)     #每次修改都会更新时间
    priority=models.IntegerField(verbose_name='优先级',default=1000)
    head_img=models.ImageField('文章图片',upload_to='uploads')
    status_choice=(
        ('draft','草稿'),
        ('published','已发布'),
        ('hidden','隐藏'),
    )
    status=models.CharField(choices=status_choice,default='published',max_length=32)
    def __str__(self):      #str用于美化输出，让函数返回我们str定义的字段，而不是返回一个内存地址对象。py2里面用__unicode__
        return self.title
    '''
    clean 用于对表里面的输入做验证，这样就不用前端去做判断了。
    如下方法：
    如果状态类型是草稿，那么就不能给这个文章的pub_date赋值，这时候就返回一个错误信息。
    如果是已发布状态且pub_date是空的，那么就给pub_date这个字段填上当前时间。
    '''
    def clean(self):
        # Don't allow draft entries to have a pub_date.
        if self.status == 'draft' and self.pub_date is not None:
            raise ValidationError(('Draft entries may not have a publication date.'))
        # Set the pub_date for published items if it hasn't been set already.
        if self.status == 'published' and self.pub_date is None:
            self.pub_date = datetime.date.today()

class Comment(models.Model):
    article=models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name='所属文章',related_name='my_comment')
    #回复评论，外键关联自己，表示和这一列里面的其它行数据关联。related_name代表让这一行可以通过my_children来反查下级关联。
    parent_comment=models.ForeignKey('self',on_delete=models.CASCADE,related_name='my_children',blank=True,null=True,verbose_name='父级评论')
    comment_choice=(
        (1,'评论'),
        (2,'点赞')
                    )
    comment_type=models.IntegerField(choices=comment_choice,default=1)
    user=models.ForeignKey('UserProfile',on_delete=models.CASCADE,verbose_name='用户')
    date=models.DateTimeField(auto_now_add=True)
    #内容比较多的大文本就用TextField，用CharField就不合适了。
    comment=models.TextField('评论',blank=True,null=True)

    def __str__(self):
        '''
        这里的返回将影响django后台父级评论列的显示。
        parent_comment,comment两个都定义时，会把多级父评论都显示。可以看到该评论的所有层级
        只定义comment时，则只会显示评论上级父评论，而上上级等则不会再显示
        '''
        # return '%s'%(self.comment)
        return '%s,%s'%(self.parent_comment,self.comment)
    def clean(self):
        # if self.comment_type==1 and self.comment is None:   #这里用 is None是错误的，当我们没有写评论时的值应该时''，而不是None。所以要用len来判断长度才对
        if self.comment_type==1 and len(self.comment)==0:
            raise ValidationError('评论不能为空')

class Category(models.Model):
    name=models.CharField(max_length=64,unique=True)
    brief=models.CharField(null=True,blank=True,max_length=255,verbose_name='板块介绍')
    set_as_top_menu=models.BooleanField(default=False,verbose_name='是否首页显示')
    position_index=models.SmallIntegerField(verbose_name='标题排序')
    admins=models.ManyToManyField('UserProfile',blank=True)     #blank=True表示可以为空，blank则用于做空字段的校验。
    # def __unicode__(self):      #这是python2的写法，3里面用__str__(self)
    #     return self.name
    '''定义str函数，这样在django后台的外键下拉框里面就会显示对应的name的值，而不是返回一个object的对象'''
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    #从django自带的User表里面引入用户，用户密码等信息就直接存在django后台的用户表里面了，我们这里就不用再定义了
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=32)
    signature=models.CharField(max_length=255,blank=True,null=True) #blank=True表示用户可以不填写这个字段，null=True表示允许数据库存储空字段。
    head_img=models.ImageField(height_field=150,width_field=150,blank=True,null=True)
    friends=models.ManyToManyField('self',related_name='my_friends',blank=True,null=True)
    def __str__(self):
        return self.name