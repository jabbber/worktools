#!/usr/bin/env python
# coding=utf-8
# target: find vm by mac address
# author: jabber.zhou
from __future__ import print_function

import sys
import requests
import json
from multiprocessing.dummy import Pool as ThreadPool
import functools

import paramiko

class CmdbAPI:
    def __init__(self):
        self.__API_URL = "http://api-gw.ucloudadmin.com/cmdb"
        self.__API_KEY = {"api-key":"xxxxxxxxxxxx"}
        self.__headers = self.__API_KEY

    class __response():
        def __init__(self,response):
            content = json.loads(response.text)
            self.ok = response.ok
            try:
                self.code = content['meta']['code']
                self.message = content['meta']['message']
            except:
                print(content)
            self.data = content.get('data')
            self.error = content.get('error')

    def request(self,method,url, **kwargs):
        return self.__response(requests.request(method,self.__API_URL+url,headers=self.__headers,**kwargs))

    def get(self,url,**kwargs):
        return self.request('GET',url,**kwargs)

    def post(self,url,**kwargs):
        return self.request('post',url,**kwargs)

def get_vmzone_server(idc='*'):
    cmdb = CmdbAPI()
    request = {
        "category": "Server",
        "q": 'Usage==uops;SecUsage==vmzone;State==0;IDC=={0};OperationalStatus==上线'.format(idc),
        "order": "IP asc",
        #"fields": "(IP,HostName,IDC,Location)"
        "fields": "(IP)"
    }
    r = cmdb.get('/v2/ci/search',params=request)
    return r.data

def remote_cmd(host,cmd):
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host,username='root')
        chan = client.get_transport().open_session()
        chan.exec_command(cmd)
        status = chan.recv_exit_status()
        output = chan.recv(-1)
        error = chan.recv_stderr(-1)
    return status,output,error

def findmac(host,maclist):
    cmd='''
        vm_list=`virsh list|awk '{if(NR>2) print $2}'`
        for vm in $vm_list;
        do
            mac=`virsh dumpxml $vm|grep'''
    for mac in maclist:
	cmd += " -e '{0}'".format(mac)
    cmd += '''`
            if [[ $? -eq 0 ]];then
                echo -n "$vm "
                echo $mac|awk -F"\'" '{print $2}'
            fi
        done
    '''
    return remote_cmd(host,cmd)

if __name__ == '__main__':
    #vmhosts = get_vmzone_server('HN04')
    vmhosts = get_vmzone_server(sys.argv[1])
    host_iplist = [host['IP'] for host in vmhosts]

    #macs = ["52:84:00:14:a2:06",]
    macs = sys.argv[1:]

    # 并发线程池
    pool = ThreadPool(100)
    results = pool.map(functools.partial(findmac, maclist=macs),host_iplist)
    print('{0:<16}{1:<16}{2:<22}'.format('host','vm','mac'))
    for num,result in enumerate(results):
        status, out, err = result
        if not status and out:
            for line in out.split('\n'):
                vm, mac = line.split(' ')
                vm = vm.replace('-','.')
                print('{0:<16}{1:<16}{2:<22}'.format(host_iplist[num],vm,mac))
        elif err:
            print(err)
