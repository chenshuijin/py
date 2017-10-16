#!/usr/local/bin/python3
#-*-coding:utf-8-*-
# filename:genmd.py

import help

def getmap(html):
    tables = help.gettable(html)
    table = tables[0]
    trs = help.gettr(table)
    rootdict = {}
    tmpdict = {}
    tmpKey = ""
    tmpList = []
#    print(help.washtags(trs[0]))
    for tr in trs[1:]:
        tr = help.washtr(tr)
        if (not tr) or tr == "":
            continue

        if help.isStrong(tr):
            if tmpdict:
                rootdict[tmpKey] = tmpdict
                tmpdict={}
            tmpKey = help.washtags(tr)
            tmpList = []
            continue
        tmpdict.update(gethref(tr))
    return rootdict

def gethref(tr):
    if not tr or tr == "":
        return None
    dic ={}
    tagas = help.geta(tr)
    for line in tagas:
        if not line or line == "":
            continue
        dic[help.washtags(line)]=help.gethref(line)
    return dic
