from django.db import models
from Wolf.models import UserProfile
# Create your models here.

class CommonInfo(models.Model):
    '''这是一个Model基类,下面的其它类可以继承这个类
    如果其它的类继承了该类,那么继承的类里面也就拥有
    了该类里面定义的字段,这样就避免了在每个类里面重
    复造轮子,精简了代码
    对于某些容易被各个表共用的字段适合使用该方法
    '''
    create_date = models.DateTimeField('创建时间', blank=True,null=True, auto_now_add=True)
    update_date = models.DateTimeField('更新时间', blank=True,null=True, auto_now=True)
    memo = models.CharField('备注',max_length=128, blank=True,null=True)

    class Meta:
        # abstract=True代表这是一个可以继承的基类,而不是一个普通的表.
        abstract = True


class Asset(CommonInfo):
    '''资产表,所有设备都要关联到资产表'''
    asset_type_choice = (
        ('server', u'服务器'),
        ('switch', '交换机'),
        ('router', '路由器'),
        ('firewall', '防火墙'),
        ('storage', '存储'),
        ('SLB', '负载均衡'),
        ('softwar', '软件资产'),
        ('other', '其它'),
    )
    asset_type = models.CharField(verbose_name='资产类型', choices=asset_type_choice, max_length=64)
    name = models.CharField('资产名称', max_length=64, unique=True)
    sn = models.CharField('资产SN号', max_length=128, unique=True)
    manufactory = models.ForeignKey('Manufactory', on_delete=models.SET_NULL, verbose_name='生产商',
                                    null=True)  # 外键删除时,该字段置空
    management_ip = models.GenericIPAddressField('管理IP', blank=True,null=True,unique=True)
    contract = models.ForeignKey('Contract', on_delete=None, verbose_name='合同', blank=True,
                                 null=True)  # 其实null=True是不需要的,只写blank=True即可
    trade_date = models.DateField('购买时间', null=True, blank=True)
    expire_date = models.DateField('过保时间', null=True, blank=True)
    price = models.FloatField('价格', null=True, blank=True)
    bussiness_unit = models.ForeignKey('BussinessUnit', on_delete=models.SET_NULL, verbose_name='所属业务', null=True,
                                       blank=True)
    tags = models.ManyToManyField('Tag', verbose_name='标签', blank=True,null=True)
    admin = models.ForeignKey(UserProfile, on_delete=models.SET_DEFAULT, verbose_name='资产管理员',
                              default=1)  # 外键删除时,该字段变默认值1
    idc = models.ForeignKey('IDC', on_delete=models.SET_NULL, verbose_name='IDC机房', blank=True,null=True)

    class Meta:
        '''verbose_name表示给表起一个可读的名字'''
        verbose_name = '资产总表'  # 给这个表起一个可读的名字
        verbose_name_plural = '资产总表'  # 这个表的复数形式叫什么,如果不写,默认会是verbose_name+s

    def __str__(self):
        return f'id:{self.id},name:{self.name}'


class Server(CommonInfo):
    '''服务器表'''
    # 只能在Server里面写一对一关联到Asset,不能反过来在Asset里面一对一关联Server
    # 因为Asset表可能被多个表一对一的关联,而OneToOneField字段在一个类里面只能写一次
    # 所以,如果写在Asset里面,那Asset就只能关联一个表了
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    # 定义是手动添加的还是自动添加的
    created_by_choice = (
        ('auto', 'Auto'),
        ('manual', 'Manual'),
    )
    created_by = models.CharField('创建方式', choices=created_by_choice, max_length=32)
    # hosted_on主要用于虚拟机资产,虚拟机是建立在一台宿主机上的,所以它应该是自关联到该字段的宿主机的.
    # 这里定义了CASCADE,即当宿主机删除的时候,这个虚拟机的字段也对应着删除了.
    hosted_on = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='宿主机', related_name='vm',blank=True,null=True)
    model = models.CharField('型号', max_length=128, null=True, blank=True)
    raid_type = models.CharField('raid类型', max_length=32, blank=True,null=True)
    os_type = models.CharField('操作系统类型', max_length=32)
    os_distribution = models.CharField('发行版本', max_length=64, blank=True,null=True)
    os_release = models.CharField('操作系统版本', max_length=64, blank=True,null=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'

    def __str__(self):
        '''返回外键关联的服务器名称以及sn号'''
        #return f'{self.asset.sn},{self.asset.name}'
        return self.os_type


class Cpu(CommonInfo):
    asset = models.OneToOneField('Asset', on_delete=models.CASCADE)
    cpu_model = models.CharField('cpu型号', max_length=64, blank=True,null=True)
    cpu_count = models.SmallIntegerField('物理cpu个数')
    cpu_core_count = models.SmallIntegerField('cpu核数')
    memo = models.CharField('备注', max_length=128,blank=True,null=True)

    class Meta:
        verbose_name_plural = 'CPU'
        verbose_name = 'CPU'

    def __str__(self):
        return self.cpu_model


class Disk(CommonInfo):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField('SN号', max_length=128, blank=True,null=True)
    slot = models.CharField('插槽', max_length=64)
    model = models.CharField('型号', max_length=64, blank=True,null=True)
    manufactory = models.ForeignKey('Manufactory', on_delete=models.SET_NULL, verbose_name='生产商', blank=True,null=True)
    capacity = models.FloatField('磁盘容量GB')
    disk_iface_type = (
        ('STAT', 'STAT'),
        ('SCSI', 'SCSI'),
        ('SAS', 'SAS'),
        ('SSD', 'SSD'),
    )
    iface_type = models.CharField('磁盘类型', choices=disk_iface_type, max_length=32, default='SAS')
    auto_create_fields = ['sn','slot','manufactory','model','capacity','iface_type']

    class Meta:
        # 一台机器上的硬盘插槽是不可能重的,所以可以利用机器和插槽设置联合唯一
        unique_together = ('asset', 'slot')  # 设置联合唯一,不能出现两条asset以及slot都一样的数据
        verbose_name_plural = '硬盘'
        verbose_name = '硬盘'

    def __str__(self):
        return f'{self.asset_id}:slot:{self.slot} capacity:{self.capacity}'


class Ram(CommonInfo):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField('SN号', max_length=128, blank=True,null=True)
    slot = models.CharField('插槽', max_length=64)
    model = models.CharField('型号', max_length=64, blank=True,null=True)
    manufactory = models.ForeignKey('Manufactory', on_delete=models.SET_NULL, verbose_name='生产商', blank=True,null=True)
    capacity = models.FloatField('内存大小GB')
    auto_create_field = ['sn', 'slot', 'manufactory', 'capacity', 'capacity']

    class Meta:
        unique_together = ('asset', 'slot')
        verbose_name_plural = '内存'
        verbose_name = '内存'

    def __str__(self):
        return f'{self.asset_id}:slot:{self.slot} capacity:{self.capacity}'


class Nic(CommonInfo):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    name = models.CharField('网卡名', max_length=64, blank=True,null=True)
    sn = models.CharField('SN号', max_length=128, blank=True,null=True)
    model = models.CharField('网卡型号', max_length=64, blank=True,null=True)
    macaddress = models.CharField('MAC地址', max_length=64, unique=True)
    ipaddress = models.GenericIPAddressField('IP地址', blank=True, null=True)
    netmask = models.CharField('子网掩码', max_length=64, blank=True,null=True)
    bonding = models.CharField(max_length=64, blank=True,null=True)

    auto_create_fields = ['name', 'sn', 'model', 'macaddress', 'ipaddress', 'netmask', 'bonding']

    class Meta:
        # unique_together=('asset','slot')
        verbose_name_plural = '网卡'
        verbose_name = '网卡'

    def __str__(self):
        return f'{self.asset_id}:{self.macaddress}:{self.asset_id}'


class RaidAdaptor(CommonInfo):
    name = models.CharField('网卡名', max_length=64, blank=True,null=True)
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    sn = models.CharField('SN号', max_length=128, blank=True,null=True)
    slot = models.CharField('插槽', max_length=64)
    model = models.CharField('RAID型号', max_length=64, blank=True,null=True)

    class Meta:
        unique_together = ('asset', 'slot')
        verbose_name_plural = '网卡'
        verbose_name = '网卡'

    def __str__(self):
        return self.name


class NetworkDevice(CommonInfo):
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE)
    vlan_ip = models.GenericIPAddressField('VlanIP', blank=True,null=True)
    intranet_ip = models.GenericIPAddressField('内网IP', blank=True,null=True,unique=True)
    sn = models.CharField('SN号', max_length=128, blank=True,null=True)
    model = models.CharField('型号', max_length=64, blank=True,null=True)
    fireware = models.ForeignKey('Software', on_delete=models.SET_NULL, null=True, blank=True)  # 固件型号,操作系统版本
    port_num = models.SmallIntegerField('端口个数', blank=True,null=True)
    device_detail = models.TextField('设置详细配置', blank=True,null=True)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = '网络设备'


class Software(CommonInfo):
    os_type_choice = (
        ('linux', 'Linux'),
        ('windows', 'Windows'),
        ('network_firware', 'Network Firware'),
        ('software', 'Software'),
    )
    os_distribution_choices = (
        ('windows', 'Windows'),
        ('centos', 'Centos'),
        ('ubuntu', 'Ubuntu'),
    )
    type = models.CharField('系统类型',max_length=32, choices=os_type_choice)
    distribution = models.CharField('发行版本', max_length=64,choices=os_distribution_choices)
    version = models.CharField('软件及系统版本', max_length=64, blank=True,null=True)
    language_choices = (('cn', '中文'), ('en', '英语'),)
    language = models.CharField('系统语言', max_length=32, choices=language_choices)

    class Meta:
        verbose_name = '软件及系统'
        verbose_name_plural = '软件及系统'

    def __str__(self):
        return self.version


class Manufactory(models.Model):
    manufactory = models.CharField('厂商名称', max_length=128, unique=True)
    support_num = models.CharField('支持电话', max_length=16, blank=True,null=True)
    memo = models.CharField('备注', max_length=128, blank=True,null=True)

    def __str__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = '厂商'


class BussinessUnit(models.Model):
    # 由于业务可能会有分层,大的业务线下面会有细分的业务线,所以会有一个层级的关联关系,所以这里外键关联了自己
    parent_unit = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent_level', blank=True,null=True)
    name = models.CharField('业务线', max_length=64, unique=True)
    memo = models.CharField('备注', max_length=128, blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '业务线'
        verbose_name = '业务线'


class Contract(CommonInfo):
    sn = models.CharField('合同号', max_length=128, unique=True)
    name = models.CharField('合同名称', max_length=64)
    price = models.IntegerField('合同金额')
    detail = models.TextField('合同详情', blank=True,null=True)
    start_date = models.DateField(blank=True,null=True)
    end_date = models.DateField(blank=True,null=True)
    license_num = models.IntegerField('license数量', blank=True,null=True)

    class Meta:
        verbose_name_plural = '合同'
        verbose_name = '合同'

    def __str__(self):
        return self.name


class Idc(models.Model):
    name = models.CharField('机房名称', max_length=64, unique=True)
    memo = models.CharField('备注', max_length=128, blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '机房'
        verbose_name = '机房'


class Tag(models.Model):
    '''打标签,这个功能其实很有用
    我们的资产其实有很多种分类方式,比如按
    机房分类/业务分类/操作系统分类/部门分类
    所以这些分类是很多的,你也无法确定今后会用什么分类,所以最好的方式是
    弄一个标签栏,让用户自己去分类,想怎么分就怎么打标签即可
    '''
    name = models.CharField('tag名称', max_length=128, unique=True)
    creater = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventLog(models.Model):
    name = models.CharField('事件名称', max_length=128)
    event_type_choice = (
        (1, '硬件变更'),
        (2, '新增配置'),
        (3, '设备下线'),
        (4, '设备上线'),
        (5, '定期维护'),
        (6, '业务上线\更新\变更'),
        (7, '其它'),
    )
    event_type = models.SmallIntegerField('事件类型', choices=event_type_choice)
    asset = models.ForeignKey('Asset',on_delete=models.DO_NOTHING)
    component = models.CharField('事件子项', max_length=255, blank=True,null=True)
    detail = models.TextField('事件详情')
    date = models.DateTimeField('事件时间', auto_now_add=True)
    user = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING,verbose_name='事件处理人')
    memo = models.TextField('备注', blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'

    def colored_event_type(self):
        if self.event_type == 1:
            cell_html = '<span style="background:orange;">'
        elif self.event_type == 2:
            cell_html = '<span style="background:yellowgreen;">'
        else:
            cell_html = '<span>%s</span>'
        return cell_html % self.get_event_type_display()

    colored_event_type.allow_tags = True
    colored_event_type.short_description = '事件类型'


class NewAssetApprovalZone(models.Model):
    '''新资产暂存表,
    管理员可在通过这个表看到新资产的一些信息,主要数据是存在在data列里面.
    '''
    asset_type_choice = (
        ('server', u'服务器'),
        ('switch', '交换机'),
        ('router', '路由器'),
        ('firewall', '防火墙'),
        ('storage', '存储'),
        ('SLB', '负载均衡'),
        ('softwar', '软件资产'),
        ('other', '其它'),
    )
    model = models.CharField(max_length=128, blank=True, null=True)
    asset_type = models.CharField(verbose_name='资产类型', choices=asset_type_choice, max_length=64)
    name = models.CharField('资产名称', max_length=64, unique=True)
    sn = models.CharField('资产SN号', max_length=128, unique=True)
    manufactory = models.CharField('生产商',max_length=64,null=True)
    idc = models.CharField('IDC机房',max_length=64, blank=True,null=True)
    ram_size = models.IntegerField(blank=True,null=True)
    cpu_model = models.CharField(max_length=128, blank=True,null=True)
    cpu_count = models.IntegerField(blank=True,default=1)
    cpu_core_count = models.IntegerField(blank=True,null=True)
    data = models.TextField('资产数据')
    date = models.DateTimeField('汇报时间', auto_now_add=True)
    approved = models.BooleanField('已批准', default=False)
    approved_by = models.CharField('审批人',max_length=16,blank=True,null=True)
    approved_date=models.DateTimeField('审批时间',auto_now_add=True)
    os_type = models.CharField(max_length=64, blank=True,null=True)
    os_release = models.CharField(max_length=64, blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        verbose_name = '待审批资产'
        verbose_name_plural = '待审批资产'

    def __str__(self):
        return f'{self.sn}, {self.name}'
