#!/usr/local/bin/python3
#-*-coding:utf-8-*-
# filename:main.py
import urllib.request
import re
import help
import genmd
import sys
import platform
#print (sys.getfilesystemencoding())

baseurl = 'http://www.runoob.com/linux/'
url = 'http://www.runoob.com/linux/linux-command-manual.html'

def verbose():
    print(platform.machine())
    print(platform.system())
    print(platform.platform())
    print(platform.node())

def gethtmlfromweb():
    html = help.gethtmlfromweb(url)
    help.savehtmltofile(html, 'html')

html = help.readfromhtml('html')

#print (trs1)
#for tr in range trs.group():
#    print (tr)
#print (trs[0])

cmddict = genmd.getmap(html)

url1 = ""
for key in cmddict:
    for cmd, cmdurl in cmddict[key].items():
#        print(cmd)
#        print(baseurl+cmdurl)
        url1 = baseurl+cmdurl

print(url1)
#print(help.gethtmlfromweb(url1))
print(help.gethtmlfromweb(url1))
#print(help.gethtmlfromweb(url))
