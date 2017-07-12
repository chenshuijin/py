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
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j][0] == 255:
                a[i][j]=[0,0,0]
            else:
                a[i][j] = [255,255,255]
    im = Image.fromarray(a)
    im.show()
    return pytesseract.image_to_string(im)

def devide():
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

def devideCode(f):
    table = devide()
    im = Image.open(f)
    # convert to grey-scale map
    imgry = im.convert('L')
    # save image
    # imgry.save('g'+f)
    # devide
    out = imgry.point(table, '1')
    # out.save('b', f)
    text = pytesseract.image_to_string(out)
    return text

print ('-----simple code----')
print (simpleCode('./images/20169992024422.png'))
print (simpleCode('./images/7025.jpg'))
print ('-----double code----')
print (doubleCode('./images/20169992024422.png'))
print (doubleCode('./images/7025.jpg'))
print ('-----devide code----')
print (devideCode('./images/20169992024422.png'))
print (devideCode('./images/7025.jpg'))

print (Image.open('./images/7025.jpg'))
