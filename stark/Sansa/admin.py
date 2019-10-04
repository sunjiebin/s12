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
    exclude = ('memo',)
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
    inlines = [ServerInline,CpuInline,RamInline,NicInline]
    search_fields = ['sn',]
    list_filter = ['idc','name','manufactory','asset_type']
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
    list_display = ('sn','asset_type')
    actions = ['approve_selected_objects']
    def approve_selected_objects(modeladmin,request,queryset):
        selected=request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct=ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect('/asset/new_asset/approval/')
    approve_selected_objects.short_description = '批准入库'


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



