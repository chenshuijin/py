#!/usr/local/bin/python3

__author__ = 'chenshuijin'

import json, hashlib,struct,time,sys, hmac
import urllib.request

class zb_api:

    def __init__(self, secretKey, accessKey):
        self.accessKey = accessKey
        self.secretKey = secretKey

    def calcHmacSign(self, params):
        sha1 = hashlib.sha1()
        sha1.update(self.secretKey.encode('utf-8'))
        shaKey = sha1.hexdigest().encode('utf-8')

        hc = hmac.new(shaKey)
        hc.update(params.encode('utf-8'))
        return hc.hexdigest()

    def __api_call(self, path, params = ''):
        try:
            sign = self.calcHmacSign(params)
            reqTime = (int)(time.time()*1000)
            params += '&sign=%s&reqTime=%d'%(sign, reqTime)
            url = 'https://trade.zb.com/api/' + path + '?' + params
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req, timeout=2)
            doc = json.loads(res.read())
            return doc
        except Exception as ex:
            print(sys.stderr, 'zb request ex: ', ex)
            return None

    def query_account(self):
        try:
            params = "accesskey="+self.accessKey+"&method=getAccountInfo"
            path = 'getAccountInfo'

            obj = self.__api_call(path, params)
            #print obj
            return obj
        except Exception as ex:
            print(sys.stderr, 'zb query_account exception,',ex)
            return None


if __name__ == '__main__':
    f = open('keys.json', 'r', encoding='UTF-8')
    keys = f.read()
    f.close()
    ks=json.loads(keys)
    print("ks:", ks)
    access_key    = ks['access_key']
    access_secret = ks['access_secret']
    api = zb_api(access_secret, access_key)
    print(api.query_account())
