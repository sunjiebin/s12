#!/usr/bin/env python
# --- coding:utf-8 ---
print ('hello word!')
import getpass
a=getpass.getpass('input pass:')
if a == 'sun':
    print "that's %s"%(a)
    if a is 'sun':
        print id(a)
        print id('sun')
    else:
        print 'a id not sun id'
        print "a's id is %s"%(id(a))
        print "sun's id is {expect}".format(expect=id('sun'))
        print "a is {aid},sun is {sunid}".format(aid=id(a),sunid=id('sun'))
else:
    print '{name} is not {sun}'.format(name=a,sun='sun')
print 'ok'
