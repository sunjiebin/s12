#!/usr/bin/env python3
# Python version: python3
# Auther: sunjb
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
def print_err(msg,quit=False):
    output = "\033[31;1mError: %s\033[0m" % msg
    if quit:
        exit(output)
    else:
        print(output)

def yaml_parser(filename):
    try:
        yaml_file=open(filename,'r')
        data=yaml.load(yaml_file)
        return data
    except Exception as e:
        print_err(e)