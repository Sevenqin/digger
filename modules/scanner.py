#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nmap
import sys
import re
import threadpool

scanner_results_path = sys.path[0]+'/scanner_results.txt'
CONFIGS = {}
scan_result = []

def __subScanList(ip):
    ipsplitArr = ip.split('.')
    if(len(ipsplitArr)!=4):
        return []
    rangeResult = []
    result = []
    for i in range(len(ipsplitArr)):
        ipsplit = ipsplitArr[i]
        index = 0
        try:
            index = ipsplit.index('-')
        except:
            index = -1
        if index>0:
            begin = int(ipsplit[:index])
            end = int(ipsplit[index+1:])
            rangeResult.append({'begin':begin,'end':end})
        else:
            begin = int(ipsplit)
            end = int(ipsplit)
            rangeResult.append({'begin':begin,'end':end})
    for i0 in range(rangeResult[0]['begin'],rangeResult[0]['end']+1):
        for i1 in range(rangeResult[1]['begin'],rangeResult[1]['end']+1):
            for i2 in range(rangeResult[2]['begin'],rangeResult[2]['end']+1):
                for i3 in range(rangeResult[3]['begin'],rangeResult[3]['end']+1):
                    result.append(str(i0)+'.'+str(i1)+'.'+str(i2)+'.'+str(i3))
    return result

def getScannerList(hostsArr):
    regularHostsList = []
    for hosts in hostsArr:
    # 如果是ip则直接加进去
        arr = str.split(hosts,'/')
        if len(arr) == 1:
            subScanList = __subScanList(arr[0])
            for subip in subScanList:
                regularHostsList.append(subip)
        elif len(arr) == 2:
            # 解析其中的地址段
            subScanList = __subScanList(arr[0])
            for subip in subScanList:
                regularHostsList.append(subip+'/'+arr[1])
    return regularHostsList

def resultCallback(workrequest,result):
    scan_result = getScannerResult()
    for resultDic in result:
        scan_result.append(resultDic)

def scanner(l):
    print('start scan: '+l+'\n')
    # 获取扫描端口
    ports = CONFIGS['ports']
    portsArr = []
    for (k,v) in ports.items():
        portsArr.append(k)
    ports = ','.join(portsArr)
    nm = nmap.PortScanner()
    nm.scan(hosts=l,arguments='-T4 -A -sS -p'+ports)
    f=open(scanner_results_path,'a')
    f.write(nm.csv())
    f.close()
    # 将打开的端口信息append到scan_result中
    scan_result = getScannerResult()
    hostsList = []
    for host in nm.all_hosts():
        if nm[host].state()== 'up':
            for port in nm[host]['tcp'].keys():
                if nm[host]['tcp'][port]['state']=='open':
                    hostsList.append({'host':host,'port':port,'hostname':nm[host].hostname(),'name':nm[host]['tcp'][port]['name']})
    return hostsList

def getScannerResult():
    global scan_result
    return scan_result


def scanByConfig(configs):
    hostsArr = []
    global CONFIGS
    CONFIGS = configs
    for host in configs['hosts']:
        hostsArr.append(host)
    hosts = getScannerList(hostsArr)
    f=open(scanner_results_path,'a')
    f.truncate()
    f.close()
    pool = threadpool.ThreadPool(int(configs['threads']))
    requests = threadpool.makeRequests(scanner, hosts,callback=resultCallback)
    [pool.putRequest(req) for req in requests]
    pool.wait()
    pool.dismissWorkers(int(configs['threads']))
    return getScannerResult()
