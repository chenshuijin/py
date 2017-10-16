#!/usr/local/bin/python3
#-*-coding:utf-8-*-
# filename:help.py
import urllib.request
import re
import zlib

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
    response.headers.get('Content-Encoding')
    html = response.read()
    if response.headers.get('Content-Encoding'):
        html = zlib.decompress(html, 16+zlib.MAX_WBITS)
    response.close()
    return html.decode('utf-8')

def gettable(s):
    ptable = re.compile('<table[\s\S]*</table>')
    return ptable.findall(s)

def gettr(s):
    ptr = re.compile('<tr.*>', re.M|re.I)
    tr = ptr.findall(s)[0]
    if tr:
        ptr = re.compile('</tr>', re.M|re.I)
        return ptr.split(s)
    else:
        return None

def geta(s):
    pa = re.compile('</a>', re.M|re.I)
    if s:
        return pa.split(s)
    else:
        return None

def washtr(s):
    if s:
        pt = re.compile('</?t.*?>|(&nbsp;)*', re.M|re.I)
        return pt.sub("",s).strip()
    else:
        return s

def gethref(s):
    if s:
        pt = re.compile('href=.*"', re.M|re.I)
        return pt.findall(s)[0].replace("href=\"", "").replace('"','')
    else:
        return s


def washtags(s):
    if s:
        pt = re.compile('<.*?>|(&nbsp;)*', re.M|re.I)
        return pt.sub('',s).strip()
    else:
        return s

def isStrong(s):
    return 'strong' in s.lower()
