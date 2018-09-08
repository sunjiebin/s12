#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from models import models
from conf import settings
from modules.utils import print_err,yaml_parser
from modules.db_conn import engine,session

'''用于定义所有逻辑处理'''
def syncdb(argvs):
    print("Syncing DB....")
    engine = models.create_engine(settings.ConnParams,
                          echo=True )
    models.Base.metadata.create_all(engine) #创建所有表结构

def create_hosts(argvs):
    '''读取参数中的yaml文件并解析'''
    if '-f' in argvs:
        hosts_file=argvs[argvs.index('-f')+1]
    else:
        print_err("create_hosts -f <the hosts file>",quit=True)
    source=yaml_parser(hosts_file)
    if source:
        for key,val in source.items():
            print(key,val)
            obj=models.Host(hostname=key,ip=val.get('ip'),port=val.get('port') or 22,)
            session.add(obj)
        session.commit()
def create_remoteusers(argvs):
    '''创建远程主机用户'''
    if '-f' in argvs:
        remoteusers_file=argvs[argvs.index('-f')+1]
    else:
        print_err('create_remoteusers -f <the remote user file>',quit=True)
    source=yaml_parser(remoteusers_file)
    if source:
        for key,val in source.items():
            print(val)
            obj=models.RemoteUser(auth_type=val.get('auth_type'),username=val.get('username'),password=val.get('password'),)
            session.add(obj)
    session.commit()

def create_users(argvs):
    '''创建堡垒机用户'''
    if '-f' in argvs:
        user_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be:\ncreateusers -f <the new users file>", quit=True)

    source = yaml_parser(user_file)
    if source:
        for key, val in source.items():
            print(key, val)
            obj = models.UserProfile(username=key, password=val.get('password'))

            session.add(obj)
        session.commit()

def create_groups(argvs):
    '''
    创建主机组
    '''
    if '-f' in argvs:
        group_file  = argvs[argvs.index("-f") +1 ]
    else:
        print_err("invalid usage, should be:\ncreategroups -f <the new groups file>",quit=True)
    source = yaml_parser(group_file)
    if source:
        for key,val in source.items():
            print(key,val)
            obj = models.HostGroup(name=key)
            # if val.get('bind_hosts'):
            #     bind_hosts = common_filters.bind_hosts_filter(val)
            #     obj.bind_hosts = bind_hosts
            #
            # if val.get('user_profiles'):
            #     user_profiles = common_filters.user_profiles_filter(val)
            #     obj.user_profiles = user_profiles
            session.add(obj)
        session.commit()

def create_bindhosts(argvs):
    if '-f' in argvs:
        bindhosts_file = argvs[argvs.index("-f") + 1]
    else:
        print_err("invalid usage, should be:\ncreate_hosts -f <the new bindhosts file>", quit=True)
    source = yaml_parser(bindhosts_file)
    if source:
        for key, val in source.items():
            print(key,val)
            host_obj = session.query(models.Host).filter(models.Host.hostname == val.get('hostname')).first()
            assert host_obj
            print(host_obj)
            '''注意下面的for语句，实际上val['remote_users']返回的是一个列表（yaml中如果有-，则变成列表），然后列表里面嵌套了字典，
            所以for其实是对列表进行了循环，而列表里面的元素则是一个个字典'''
            for item in val['remote_users']:
                print('remote_users is',item)
                '''assert断言，表示如果没有auth_type这个key，或取不到auth_type这个的值，则下面语句不执行。'''
                assert item.get('auth_type')
                if item.get('auth_type') == 'ssh-password':
                    remoteuser_obj=session.query(models.RemoteUser).filter(
                        models.RemoteUser.username==item.get('username'),
                        models.RemoteUser.password==item.get('password'),
                        #models.RemoteUser.auth_type==item.get('auth_type'),
                    ).first()
                else:
                    remoteuser_obj=session.query(models.RemoteUser).filter(
                        models.RemoteUser.username==item.get('username'),
                        models.RemoteUser.auth_type==item.get('auth_type'),
                    ).first()
                if not remoteuser_obj:
                    print_err('user [%s] is not exist'%(item),quit=True)
                bindhost_obj=models.BindHost(host_id=host_obj.id,remoteuser_id=remoteuser_obj.id)
                session.add(bindhost_obj)
                '''判断是否有groups这个字段，如果有则执行下面语句'''
                if source[key].get('groups'):
                    print(source[key].get('groups'))
                    group_objs=session.query(models.HostGroup).filter(
                        models.HostGroup.name.in_(source[key].get('groups'))
                    ).all()
                    assert group_objs
                    '''通过下面语句将bind_host和host_group两个表的关联表bindhost_m2m_hostgroup建立起来，
                    将两个表相对应的主机和组的id相对应起来，实现主机和组的关联。
                    注意下面的语句将对关联表插入相关联的ID值'''
                    bindhost_obj.host_groups=group_objs

                if source[key].get('user_profiles'):
                    user_objs=session.query(models.UserProfile).filter(
                        models.UserProfile.username.in_(source[key].get('user_profiles'))
                    ).all()
                    assert user_objs
                    '''通过下面的语句，将堡垒机用户表和bind_host表相关联起来，对两者的关联表user_m2m_bindhost
                    插入对应的两方id，通过该表的外键实现两表关联，最终实现用户和主机关联'''
                    bindhost_obj.user_profiles=user_objs
        session.commit()
        # user_m2m_bindhost=session.query(models.user_m2m_bindhost).all()
        # group_m2m_bindhost=session.query(models.bindhost_m2m_hostgroup).all()
        # print(user_m2m_bindhost)
        # print(group_m2m_bindhost)



