#!/usr/bin/python3
#-*-coding:utf-8-*-
# filename:main.py
import urllib.request
import re
import sys
import platform
import sha3
import json
import os.path
import time
#print (sys.getfilesystemencoding())

apiurl = 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock=379224&toBlock=latest&address=0x06012c8cf97BEaD5deAe237070F9587f8E7A266d&apikey=YourApiKeyToken'

daystart = 24
totaldays = 20
dayofblocks = 5958

def verbose():
    print(platform.machine())
    print(platform.system())
    print(platform.platform())
    print(platform.node())


def downloadtxs(name, item):
    for i in range(totaldays):
        for adr in item['address']:
            filename ='./data/'+ parsefilename(name,(daystart-i),adr,item['fromBlock']-5863*i,item['toBlock']-5863*i)
            url = parseurl(item['fromBlock'], item['toBlock'], adr)
#            print('url:', url)
            print('filename:', filename)
            download(filename, url)
            time.sleep(2)


def download(filename, url):
    data = getHttpResp(url).decode('utf-8')
#    print(data)
    obj = json.loads(data)
    if obj['status'] != '1': return
    if obj['message'] != 'OK': return

    f = open(filename, 'w')
    f.write(data)
    f.close()

def getfuncsig(func):
    k = sha3.keccak_256()
    k.update(func)
    return '0x'+k.hexdigest()

def parseurl(fromBlock, toBlock, address):
    return 'https://api.etherscan.io/api?module=logs&action=getLogs&fromBlock={}&toBlock={}&address={}&apikey=YourApiKeyToken'.format(fromBlock, toBlock, address)

def parsefilename(tokenname,day,address, _from, to):
    return '{}4月{}日{}from:{}to:{}tx'.format(tokenname,day, address, _from, to)


def getHttpResp(url):
    response = urllib.request.urlopen(url)
    resp = response.read()
    return resp

def process(filename, target):
    if os.path.exists(filename)==False:
        return 0

    f = open(filename, 'r')
    data = f.read()
    f.close()
    data = json.loads(data)['result']
    counter = 0

    for i in data:
        if target in i['topics']:
            counter += 1

    return counter


def process20(name, item):
    for i in range(totaldays):
        for adr in item['address']:
            filename ='./data/'+ parsefilename(name,(daystart-i),adr,item['fromBlock']-5863*i,item['toBlock']-5863*i)
            counter = process(filename,transfersig)
            if counter > 0 : print('%s %s日tansfer %s' % (name, (daystart-i),counter))
            counter = process(filename,transfersig721)
            if counter > 0 : print('%s %s日tansfer721 %s' % (name, (daystart-i),counter))

def getconf():
    f = open('./conf.json', 'r')
    data = f.read()
    f.close()
    conf = json.loads(data)
    return conf

def maintaindownload():
    conf = getconf()
#    downloadtxs('CryptoPunks', conf['CryptoPunks'])
    for item in conf:
        print(item)
#        if item == "ETHERBOTS":
#            downloadtxs(item, conf[item])
        downloadtxs(item, conf[item])


def main():
    conf = getconf()
    for item in conf:
        process20(item, conf[item])


func_Transfer721 = b'Transfer(address,address,uint256)'
func_Transfer20 = b'Transfer(address,uint256)'
targetsig = getfuncsig(func_Transfer721)
transfersig = getfuncsig(func_Transfer20)
transfersig721 = getfuncsig(func_Transfer721)

print(func_Transfer20, ":", transfersig)
print(func_Transfer721, ":", transfersig721)
#main()
#maintaindownload()
#print(getfuncsig(func_Transfer721))
