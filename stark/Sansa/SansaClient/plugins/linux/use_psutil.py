#!/usr/bin/env python3
# Auther: sunjb

import subprocess,sys,os

try:
    import psutil
except ImportError:
    try:
        command="pip3 install psutil || easy_install psutil"
        subprocess.getoutput(command)
    except Exception as e:
        exit('install error:',e)
    import psutil

    par


