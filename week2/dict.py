#!/usr/bin/env python
# Python version: python3
# Auther: sunjb
aa={1:2,
    'name':'sun',
    'age':18,
    'gender':'man'}
print(aa)
aa['school']='tsinghua'
print(aa)
del aa['school']
print(aa)

print(aa.keys())
print(aa.values())
print(aa.items())

for k in aa.keys():
    print(k)

for v in aa.values():
    print(v)

for k,v in aa.items():
    print(k)
    print(v)