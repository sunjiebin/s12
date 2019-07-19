from django.db import models

# Create your models here.

from django.db import models
'''
业务梳理：
文章表关联文章类型

'''
class Category(models.Model):
    caption=models.CharField(max_length=32)

class ArticleType(models.Model):
    caption=models.CharField(max_length=32)
    
class Article(models.Model):
    title=models.CharField(max_length=32)
    content=models.CharField(max_length=255)
    category=models.ForeignKey(to=Category,on_delete=models.CASCADE,)
    article_type=models.ForeignKey(ArticleType,on_delete=models.CASCADE)
    
    # 可以定义type_choice，这样这个字段的值就是固定在内存中，不会写入数据库。这对于那种用于不会变得数据很有用，减少数据库的查询操作。
    # 而article_type_id同过choice=type_choice与之关联，减少了关联查询操作。
    # type_choice=(
    #     (0,'python'),
    #     (1,'openstack'),
    #     (2,'docker'),
    # )
    # article_type_id=models.IntegerField(choices=type_choice)