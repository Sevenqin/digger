#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
# import urllib
import sys
import re

def getIPList():
    f = open('./ip_port.txt')
    l = f.readlines()
    f.close()
    return l

def getTitle(l):
    for ur in l:
        r = ''
        try:
            r = urllib2.urlopen(url='http://'+ur,timeout=2)

            match = re.findall(r"<title>(.+?)</title>",r.read())
            if match:
                print ur.strip('\n')+'\t'+match[0]
                
        except:
            a=1


if __name__ == '__main__':
    l = getIPList()
    getTitle(l)
