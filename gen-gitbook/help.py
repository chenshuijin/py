#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# filename:help.py

import urllib.request
import re

def savehtmltofile(html, fi):
    f = open(fi, 'w')
    f.write(html)
    f.close()

def readfromhtml(fi):
    f = open(fi, 'r')
    lines = f.read()
    f.close()
    return lines

def gethtmlfromweb(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    response.close()
    html =  html.decode("utf-8")
    return html

def gettable(s):
    ptable = re.compile('<table[\s|\S]*</table>')
    return ptable.findall(s)

def gettr(s):
    ptr = re.compile('<tr[\s|\S]*</tr>')
    return ptr.search(s)
