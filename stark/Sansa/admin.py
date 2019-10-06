from django.contrib import admin
from Sansa import models
# Register your models here.

class ServerInline(admin.TabularInline):
    model = models.Server
    #定义被别的表引用编辑时,排除编辑的字段,这些字段不会出现在关联编辑中
    exclude = ('memo','hosted_on','os_distribution')
    #定义不可编辑字段
    readonly_fields = ['create_date','created_by']
class CpuInline(admin.TabularInline):
    model = models.Cpu
    exclude = ('memo',)
   # readonly_fields = ['create_date']
class NicInline(admin.TabularInline):
    model = models.Nic
    exclude = ('memo','bonding','sn','netmask')
    readonly_fields = ['create_date']
class RamInline(admin.TabularInline):
    model = models.Ram
    exclude = ('memo',)
    readonly_fields = ['create_date']
class DiskInline(admin.TabularInline):
    model = models.Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']
class AssetAdmin(admin.ModelAdmin):
    #list_display定义在admin后台里面显示该表的哪些列
    list_display = ('id','asset_type','sn','name','manufactory','management_ip','idc','bussiness_unit')
    # inlines表示允许在修改asset表时,同时可以修改以下表的列
    # 注意被Inline的表都要和该表有外键关联才能inline,如果没有是不能写inlines的
    inlines = [ServerInline,CpuInline,RamInline,NicInline]
    search_fields = ['sn',]
    list_filter = ['idc','name','manufactory','asset_type']
class ServerAdmin(admin.ModelAdmin):
    #list_display定义在admin后台里面显示该表的哪些列
    list_display = ('id','created_by','hosted_on','model','raid_type','os_type')
    #search_fields = ['sn',]
    #list_filter = ['idc','name','manufactory','asset_type']
class NicAdmin(admin.ModelAdmin):
    list_display = ('name','macaddress','ipaddress',)
    search_fields = ['ipaddress']
class EventLogAdmin(admin.ModelAdmin):
    list_display = ('name','event_type','asset')
    search_fields = ['asset']
    list_filter = ('name','event_type','date','user')

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = ('sn','asset_type','manufactory','model','cpu_model','cpu_count','cpu_core_count','ram_size','os_distribution','os_release','date','approved','approved_by','approved_date')
    actions = ['approve_selected_objects']

    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME) #得到后台选中标签的id,比如选中后台admin第一条资产,那id就是1
        print("query set model ",selected)
        ct = ContentType.objects.get_for_model(queryset.model)
        '''ct.pk实际上是django_content_type表里面对应newassetapprovalzone数据的id.
        django_content_typ表存放了app名到表名的映射关系,通过这个映射关系找到对应的app下的表'''
        print("ct ", ct,ct.pk, type(ct))
        '''下面的join是将上面选择的selected拼接起来,比如我们在admin后台同时选中了两个资产批准入库,生成的链接就是?ct=18&ids=2,1'''
        return HttpResponseRedirect("/asset/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    approve_selected_objects.short_description = "批准入库"

admin.site.register(models.Server)
admin.site.register(models.Asset,AssetAdmin)
admin.site.register(models.NetworkDevice)
admin.site.register(models.Idc)
admin.site.register(models.Cpu)
admin.site.register(models.Disk)
admin.site.register(models.Ram)
admin.site.register(models.Tag)
admin.site.register(models.Nic,NicAdmin)
admin.site.register(models.BussinessUnit)
admin.site.register(models.Manufactory)
admin.site.register(models.Software)
admin.site.register(models.EventLog,EventLogAdmin)
admin.site.register(models.NewAssetApprovalZone,NewAssetApprovalZoneAdmin)



