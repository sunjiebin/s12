from django.contrib import admin
from webchat import models
# Register your models here.
class WebGroupAdmin(admin.ModelAdmin):
    '''list_display用于定义在后台显示的列'''
    list_display = ('name','brief','owner','max_members')


#注册类
admin.site.register(models.WebGroup,WebGroupAdmin)
