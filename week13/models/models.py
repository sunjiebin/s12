#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Index,Integer,UniqueConstraint,String,DATE,Enum,ForeignKey,Table
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import ChoiceType

engin=create_engine("mysql+pymysql://root:sunjiebin@localhost:3306/jumpserver",encoding=utf-8,max_overflow=5)
Base=declarative_base()

# host_m2m_remoteuser = Table('host_m2m_remoteuser',Base.metadata,
#                         Column('host_id',Integer,ForeignKey('host.id')),
#                         Column('remoteuser_id',Integer,ForeignKey('remote_user.id')),
#                         )
user_m2m_bindhost=Table('user_m2m_bindhost',Base.metadata,
                        Column('userprofile_id',Integer,ForeignKey('user_profile.id')),
                        Column('bindhost_id',Integer,ForeignKey('bind_host.id')),
                        )
bindhost_m2m_hostgroup=Table('bindhost_m2m_hostgroup',Base.metadata,
                        Column('hostgroup_id',Integer,ForeignKey('host_group.id')),
                        Column('bindhost_id',Integer,ForeignKey('bind_host.id')),
                        )
userprofile_m2m_hostgroup=Table('userprofile_m2m_hostgroup',Base.metadata,
                        Column('userprofile_id',Integer,ForeignKey('user_profile.id')),
                        Column('hostgroup_id',Integer,ForeignKey('host_group.id')),
                        )

class Host(Base):
    '''远程主机信息'''
    __tablename__='host'
    id=Column(Integer,primary_key=True)
    hostname=Column(String(64))
    ip=Column(String(32),unique=True)
    port=Column(Integer,default=22)
 #   remote_users=relationship('RemoteUser',secondary=host_m2m_remoteuser,backref='Hosts')
    def __repr__(self):
        return self.hostname

class BindHost(Base):
    '''绑定host/host_group/remote_user三个表之间的关联'''
    __tablename__='bind_host'
    id=Column(Integer,primary_key=True)
    host_id=Column(Integer,ForeignKey('host.id'))
    # group_id=Column(Integer,ForeignKey('host_group.id'))
    remoteuser_id=Column(Integer,ForeignKey('remote_user.id'))
    __table_args__=(UniqueConstraint('host_id','remoteuser_id',name='_host_remoteuser_uc'))
    host=relationship('Host',backref='bind_hosts')
    # group=relationship('HostGroup',backref='bind_hosts')
    remote_user=relationship('RemoteUser',backref='bind_hosts')
    def __repr__(self):
        return '<%s-%s-%s>'%(self.host.ip,self.group.name,self.remote_user.username)

class HostGroup(Base):
    '''主机组'''
    __tablename__='host_group'
    name=Column(String(64),unique=True)
    bind_hosts=relationship('BindHost',secondary='bindhost_m2m_hostgroup',backref='host_groups')
    def __repr__(self):
        return self.name

class RemoteUser(Base):
    '''远程主机用户登录信息'''
    __tablename__='remote_user'
    #建立一个联合惟一键_user_passwd_uc，将auth_type,username,password三者联合惟一，三个键组合在一起必需是惟一的
    __table_args__=(UniqueConstraint('auth_type','username','pasword',name='_user_passwd_uc'),)
    AuthTypes=[
        ('ssh-passwd','SSH/Password'),  #ssh-passwd是真正存在数据库的值，SSH/Password是通过sqlalchemy取出来时显示的值，它们之间做了映射
        ('ssh-key','SSH/KEY'),
    ]
    id=Column(Integer,primary_key=True)
    auth_type=Column(ChoiceType(AuthTypes)) #需要安装SQLAlchemy-Utils
    username=Column(String(64))
    password=Column(String(128))
    def __repr__(self):
        return self.username

class UserProfile(Base):
    '''堡垒机用户配置'''
    __tablename__='user_profile'
    id=Column(Integer,primary_key=True)
    username=Column(String(32),unique=True)
    password=Column(String(128))
    bind_hosts=relationship('BindHost',secondary='user_m2m_bindhost',backref='user_profiles')
    host_groups=relationship('HostGroup',secondary='userprofile_m2m_hostgroup',backref='user_profiles')
class AuditLog(Base):
    pass