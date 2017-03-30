#!/usr/bin/env python
# -*- coding: utf-8 -*-
from smb.SMBConnection import SMBConnection
import sys
import socket

USER_DIC_ARR = []
PASSWD_DIC_ARR = []
# 懒爆破只爆破一个后retun,避免因为空密码，造成任意密码刷屏
LAZY_EXPOLDE = False

def connectToHp(host,port):
    #查看是不是主机和port不能连接
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(10)
    try:
        sk.connect((host,port))
        sk.close()
        return True
    except Exception:
        print "\33[34mbad connection to "+host+':'+str(port)+'\33[37m'
        return False

def getUserDic():
    global USER_DIC_ARR
    return USER_DIC_ARR

def getPasswdDic():
    global PASSWD_DIC_ARR
    return PASSWD_DIC_ARR

def explode(host,port,dic):
    pass

def explodeListHp(hp):
    pass


if __name__ == '__main__':
    if len(sys.argv)!=2:
        print "please indicate the file path"
        sys.exit(2)
    file_path = sys.argv[1]
    hpArr = []
    try:
        f = open(file_path,'r')
        for hp in f.readlines():
            hpArr.append(hp.strip('\n'))
        f.close()
    except:
        print "file path ill legal"
        sys.exit(2)
    #加载字典
    f = open('../dict/smb_u.dic')
    for line in f.readlines():
        USER_DIC_ARR.append(line.strip('\n'))
    f.close()
    f = open('../dict/smb_p.dic')
    for line in f.readlines():
        PASSWD_DIC_ARR.append(line.strip('\n'))
    PASSWD_DIC_ARR.append('')
    f.close()
    #多线程爆破smb
    import threadpool
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(explodeListHp, hpArr)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    pool.dismissWorkers(10, do_join=True)
