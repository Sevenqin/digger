#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import modules.scanner as scanner
import modules.ftper as ftper
import threadpool
import modules.mysqler as mysqler
import modules.mssqler as mssqler
import modules.rdper as rdper
import modules.ssher as ssher
import os,sys

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def loadConfiguration():
    f = open(sys.path[0]+'/config.json','r')
    config_raw = f.read()
    f.close()
    config = json.JSONDecoder().decode(config_raw)
    return byteify(config)
CONFIG = loadConfiguration()
def loadDictionary():
    #加载mysql字典
    dic = {}
    username = []
    password = []
    f = open(sys.path[0]+'/dict/mysql_u.dic')
    for line in f.readlines():
        username.append(line.strip('\n'))
    f.close()
    f = open(sys.path[0]+'/dict/mysql_p.dic')
    for line in f.readlines():
        password.append(line.strip('\n'))
    password.append('')
    f.close()
    dic['mysql']={'username':username,'password':password}
    #加载mssql字典
    username = []
    password = []
    f = open(sys.path[0]+'/dict/mssql_u.dic')
    for line in f.readlines():
        username.append(line.strip('\n'))
    f.close()
    f = open(sys.path[0]+'/dict/mssql_p.dic')
    for line in f.readlines():
        password.append(line.strip('\n'))
    password.append('')
    f.close()
    dic['mssql']={'username':username,'password':password}
    #加载ftp字典
    username = []
    password = []
    f = open(sys.path[0]+'/dict/ftp_u.dic')
    for line in f.readlines():
        username.append(line.strip('\n'))
    f.close()
    f = open(sys.path[0]+'/dict/ftp_p.dic')
    for line in f.readlines():
        password.append(line.strip('\n'))
    password.append('')
    f.close()
    dic['ftp']={'username':username,'password':password}
    #加载telnet字典
    username = []
    password = []
    f = open(sys.path[0]+'/dict/telnet_u.dic')
    for line in f.readlines():
        username.append(line.strip('\n'))
    f.close()
    f = open(sys.path[0]+'/dict/telnet_p.dic')
    for line in f.readlines():
        password.append(line.strip('\n'))
    password.append('')
    f.close()
    dic['telnet']={'username':username,'password':password}
    return dic
DIC = loadDictionary()


def explodeProcess(scanitems):
    port = str(scanitems['port'])
    print 'start '+scanitems['host']+':'+port
    portsConfig = CONFIG['ports']
    if portsConfig.has_key(port):
        if portsConfig[port] == 'mysql':
            mysqler.explode(scanitems['host'],int(port),DIC['mysql'])
        if portsConfig[port] == 'mssql':
            mssqler.explode(scanitems['host'],int(port),DIC['mssql'])
        if portsConfig[port] == 'ftp':
            ftper.explode(scanitems['host'],int(port),DIC['ftp'])
        if portsConfig[port] == 'rdp':
            # rdp 不传入字典.....囧
            rdper.explode(scanitems['host'],int(port))
        if portsConfig[port] == 'telnet':
            ftper.explode(scanitems['host'],int(port),DIC['telnet'])
        # if portsConfig[port] == 'smb':
        #     ftper.explode(scanitems['host'],int(port),DIC['smb'])
    return scanitems['host']+':'+port+' finished'

def explodProcessCallback(workrequest,result):
    print result

if __name__ == '__main__':
    print 'scan start'
    scannerResults = scanner.scanByConfig(CONFIG)
    print scannerResults
    # scannerResults = [{'host': '192.168.50.38', 'hostname': '', 'port': 21, 'name': 'ftp'}, {'host': '192.168.50.29', 'hostname': '', 'port': 139, 'name': 'netbios-ssn'}, {'host': '192.168.50.29', 'hostname': '', 'port': 1433, 'name': 'ms-sql-s'}, {'host': '192.168.50.83', 'hostname': '', 'port': 21,'name': 'ftp'}, {'host': '192.168.200.5', 'hostname': '', 'port': 22, 'name': 'ssh'}, {'host': '192.168.200.6', 'hostname': '', 'port': 22,'name': 'ssh'}, {'host': '192.168.201.1', 'hostname': '', 'port': 22, 'name': 'ssh'}, {'host': '192.168.201.2', 'hostname': '', 'port': 22,'name': 'ssh'}, {'host': '192.168.50.112', 'hostname': '', 'port': 139, 'name': 'netbios-ssn'}, {'host': '192.168.50.112', 'hostname': '','port': 21, 'name': 'ftp'}, {'host': '192.168.50.112', 'hostname': '', 'port': 445, 'name': 'microsoft-ds'}, {'host': '127.0.0.1', 'hostname': 'localhost', 'port': 3307, 'name': 'mysql'}, {'host': '127.0.0.1', 'hostname': 'localhost', 'port': 445, 'name': 'microsoft-ds'}, {'host': '172.26.2.26', 'hostname': '', 'port': 3306, 'name': 'mysql'}, {'host': '172.26.2.26', 'hostname': '', 'port': 139, 'name': 'netbios-ssn'}, {'host': '172.26.2.26', 'hostname': '', 'port': 3389, 'name': 'ms-wbt-server'}, {'host': '172.26.2.26', 'hostname': '', 'port': 445, 'name': 'microsoft-ds'}, {'host': '192.168.135.219', 'hostname': '', 'port': 139, 'name': 'netbios-ssn'}, {'host': '192.168.135.219', 'hostname':'', 'port': 3389, 'name': 'ms-wbt-server'}, {'host': '192.168.135.219', 'hostname': '', 'port': 1433, 'name': 'ms-sql-s'}, {'host': '192.168.135.219', 'hostname': '', 'port': 445, 'name': 'microsoft-ds'}, {'host': '192.168.40.222', 'hostname': '', 'port': 21, 'name': 'ftp'}, {'host': '172.26.11.4', 'hostname': '', 'port': 3306, 'name': 'mysql'}, {'host': '172.26.11.4', 'hostname': '', 'port': 139, 'name': 'netbios-ssn'}, {'host': '172.26.11.4', 'hostname': '', 'port': 3389, 'name': 'ms-wbt-server'}, {'host': '172.26.11.4', 'hostname': '', 'port': 1433,'name': 'ms-sql-s'}, {'host': '172.26.11.4', 'hostname': '', 'port': 445, 'name': 'microsoft-ds'}, {'host': '192.168.135.202', 'hostname': '', 'port': 139, 'name': 'tcpwrapped'}, {'host': '192.168.135.202', 'hostname': '', 'port': 21, 'name': 'ftp'}, {'host': '192.168.135.232', 'hostname': '', 'port': 139, 'name': 'netbios-ssn'}, {'host': '192.168.135.232', 'hostname': '', 'port': 1433, 'name': 'ms-sql-s'}, {'host':'192.168.135.232', 'hostname': '', 'port': 445, 'name': 'microsoft-ds'},{'host': '172.26.11.4', 'hostname': '', 'port': 445, 'name': 'microsoft-ds'}, {'host': '192.168.135.202', 'hostname': '', 'port': 139, 'name': 'tcpwrapped'}, {'host': '192.168.135.202', 'hostname': '', 'port': 21, 'name': 'ftp'}, {'host': '192.168.135.232', 'hostname': '', 'port': 139, 'name': 'netbios-ssn'}, {'host': '192.168.135.232', 'hostname': '', 'port': 1433, 'name': 'ms-sql-s'}, {'host':'172.27.3.81', 'hostname': '', 'port': 3389, 'name': 'rdp'},{'host':'172.27.4.181', 'hostname': '', 'port': 3389, 'name': 'rdp'}]
    for dic in scannerResults:
        print dic['host']+':'+str(dic['port'])+'\t'+dic['name']
    # scannerResults = [{'host': '192.168.135.202', 'hostname': '', 'port': 21, 'name': 'ftp'}, {'host': '127.0.0.1', 'hostname': '', 'port': 3307, 'name': 'mysql'},{'host': '172.26.2.26', 'hostname': '', 'port': 3306, 'name': 'mysql'},{'host': '172.26.11.4', 'hostname': '', 'port': 3306, 'name': 'mysql'},{'host': '172.26.15.60', 'hostname': '', 'port': 3306, 'name': 'mysql'}]
    # scannerResults = [{'host': '192.168.4.1', 'hostname': '', 'port': 1433, 'name': 'ms-sql-s'}, {'host': '127.0.0.1', 'hostname': '', 'port': 3307, 'name': 'mysql'},{'host': '172.26.11.4', 'hostname': '', 'port': 3306, 'name': 'mysql'}]
    print 'scan complete'
    print 'Explode start'
    pool = threadpool.ThreadPool(10)
    requests = threadpool.makeRequests(explodeProcess, scannerResults,callback=explodProcessCallback)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    pool.dismissWorkers(int(CONFIG['threads']))
