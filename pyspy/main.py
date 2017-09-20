#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenshuijin'

import sys
import urllib
import urllib2
import websocket
import time

logFileName = time.strftime("%Y-%m-%d.log", time.localtime(time.time()))
logFile = open(logFileName,'ab+')

def getPage(url):
    resp = urllib2.urlopen(url)
    page = resp.read()
    return page

def readFromWs(url):
    ws = websocket.WebSocket()
    ws.connect(url)
    print 'begin reading...'
    ws.send("""{"event":"pusher:subscribe","data":{"channel":"market-global"}}""")
    while True :
        rs = ws.recv()
        logFile.write(rs)

# print getPage("http://www.yunbi.com/markets/ethcny")
# print getPage("https://yunbi.com/api/v2/tickers.json")
print readFromWs("wss://slanger.yunbi.com:18080/app/d2e734a0694b3cb3ed8cdcadcc6f346e?protocol=7&client=js&version=2.2.0&flash=false")

logFile.close()
print 'file close'
