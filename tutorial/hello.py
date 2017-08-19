#!/usr/bin/python
# -*- coding: UTF-8 -*-
# filename:hello.py
print "Hello, world";
print "你好,世界";

raw_input("Press the enter key to exit.");

import sys;
x = 'runoob';
sys.stdout.write(x + '\n');

tuple = ( 'abcd', 786, 2.23, 'john', 70.2 )
tinytuple = (123, 'john')
print tuple
print tinytuple
print tuple[0]
print tuple[1:3]
print tuple[2:]
print tinytuple * 2
print tuple + tinytuple

dict = {}
dict['one'] = "This is one"
dict[2] = "This is twe"
tinydict = {'name': 'john', 'code':6734, 'dept': 'sales', 3:'num 3'}
print dict
print tinydict
print tinydict[3]
print tinydict['name']
print tinydict.keys()
print tinydict.values()

