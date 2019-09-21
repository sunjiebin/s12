from django.db import models

# Create your models here.

class Host(models.Model):
    hostname=models.CharField(max_length=128,unique=True)
    key=models.TextField()
    static_choice=((0,'Waiting Approve'),
                   (1,'Accepted'),
                   (2,'Rejected'),)
    os_type_choice=(('redhat','RedHat/CentOS'),
                    ('ubuntu','Ubuntu'),
                    ('suse','Suse'),
                    ('windows','Windows'))
    status=models.SmallIntegerField(choices=static_choice,default=0)
    os_type=models.CharField(choices=os_type_choice,max_length=64,default='redhat')
    def __str__(self):
        return self.hostname


class HostGroup(models.Model):
    name=models.CharField(max_length=128,unique=True)
    hosts=models.ManyToManyField(Host,related_name='related_group',blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    '''用于生成任务id'''
    datetime=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.id
