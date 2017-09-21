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
print (len(tables))
table = tables[0]
trs = help.gettr(table)
print (trs)
print (trs.group(1))
print (trs.groups())
