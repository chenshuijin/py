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

ptable = re.compile('<table[\s|\S]*</table>')

def gettable(s):
    return ptable.findall(s)
