#!/usr/bin/env python3
# Auther: sunjb

import os
BaseDir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Params={
    'server':'127.0.0.1',
    'port':8000,
    'request_timeout':30,
    'urls':{
        'asset_report_with_no_id':'/asset/report/asset_with_no_asset_id',   #没资产向这里汇报
        'asset_report':'/asset/report', #有资产就向这里汇报
    },
    'asset_id':f'{BaseDir}/var/.asset_id',
    'log_file':f'{BaseDir}/logs/run_log',
    'auth':{
        'user':'sun@sun.com',
        'token':'abc',
    },
}