#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb

from modules import views
'''定义可执行的功能列表'''
actions={
    # 'start_session':views.start_session,
    # 'stop':views.stop_server
    'syncdb':views.syncdb,
    'create_users':views.create_users,
    'create_groups':views.create_groups,
    'create_hosts':views.create_hosts,
    'create_bindhosts':views.create_bindhosts,
    'create_remoteusers':views.create_remoteusers,
}



