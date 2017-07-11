#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'chenshuijin'

from PIL import Image
import pytesseract
from numpy import *

def simpleCode(f):
    image = Image.open(f)
    vcode = pytesseract.image_to_string(image)
    return vcode

def doubleCode(f):
    im = Image.open(f)
    im = im.convert('RGB')
    im = im.resize((200,80))
    a = array(im)
    for i in xrange(len(a)):
        for j in xrange(len(a[i])):
            if a[i][j][0] == 255:
                a[i][j]=[0,0,0]
            else:
                a[i][j] = [255,255,255]
    im = Image.fromarray(a)
    im.show()
    return pytesseract.image_to_string(im)

print '-----simple code----'
print simpleCode('./images/20169992024422.png')
print simpleCode('./images/7025.jpg')
print '-----double code----'
print doubleCode('./images/20169992024422.png')
print doubleCode('./images/7025.jpg')
