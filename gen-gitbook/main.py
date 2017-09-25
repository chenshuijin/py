#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename:main.py

import urllib.request
import re
import help

baseurl = 'http://www.runoob.com/'
url = 'http://www.runoob.com/linux/linux-command-manual.html'

html = help.readfromhtml('html')
tables = help.gettable(html)
table = tables[0]
trs = help.gettr(table)
#print (trs1)
#for tr in range trs.group():
#    print (tr)
print (trs)
print (len(trs))
