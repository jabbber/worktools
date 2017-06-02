#!/usr/bin/env python2
## -*- coding: utf-8 -*-
import csv
import json
import os,sys
import requests
import re
import ansible_facts

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

class CouchDB:
    def __init__(self,host,database,user,passwd,ssl=False,verify=False):
        self.host = host
        self.database = database
        self.user = user
        self.__passwd = passwd
        self.ssl = ssl
        self.verify = verify
        self.status = 0
    class Error(Exception):
        def __init__(self, status,content,url):
            self.status = status
            self.content = content
            self.url = url
        def __str__(self):
            return repr("%d : '%s' url='%s'"%(self.status,self.content,self.url))
    def __returnHandle(self,status,content,url,warning=()):
        self.status = status
        if 200 <= status < 300:
            pass
        elif status in warning or warning == 'all':
            print >> sys.stderr, self.Error(status,content,url)
        else:
            raise self.Error(status,content,url)
        return json.loads(content)
    def request(self,method, url ,data = None,warning=()):
        fullurl = "http"
        if self.ssl:
            fullurl += 's'
        fullurl += "://%s/%s%s"%(self.host,self.database,url)
        r =  requests.request(method,fullurl,auth=(self.user,self.__passwd),verify = self.verify, data = data)
        return self.__returnHandle(r.status_code,r.content,fullurl,warning)
    def getids(self,viewurl):
        result = self.request("GET",viewurl)
        return [row['id'] for row in result['rows']]
    def getdoc(self,id):
        return self.request("GET","/"+id,warning=(404,))
    def putdoc(self,doc):
        current = self.getdoc(doc["主机名"])
        diff = False
        for key in doc.keys():
            if doc[key] == "":
                doc.pop(key)
        if self.status == 404:
            return self.request("PUT","/"+doc['主机名'], data=jsondump(doc))
        else:
            for key in doc:
                if key.decode('utf-8') not in current:
                    diff = True
                    break
                elif doc[key].decode('utf-8') != current[key.decode('utf-8')]:
                    diff = True
                    break
            for key in current:
                if key != "_rev" and key !="_id" and key.encode('utf-8') not in doc:
                    diff = True
                    break
        if diff:
            if "_rev" in current:
                doc['_rev'] = current['_rev']
            return self.request("PUT","/"+doc['主机名'], data=jsondump(doc))
        else:
            return None
    def updatadoc(self,id,values):
        doc = self.getdoc(id)
        diff = False
        for key in doc.keys():
            if doc[key] == "":
                doc.pop(key)
        for key in values:
            if values[key]:
                if values[key] != doc.get(key):
                    diff = True
                    doc[key] = values[key]
        if diff:
            return self.request("PUT","/"+id, data=jsondump(doc) )
        else:
            return None

def getcolume(fact):
    values = {}
    values[u'内存'] = fact['ansible_memtotal_mb'] / 1024 + 1
    values[u'CPU'] = fact['ansible_processor_vcpus']
    values[u'CPU型号'] = fact['ansible_processor'][1]
    values[u'虚拟化'] = fact['ansible_virtualization_role']
    values[u'虚拟化类型'] = fact['ansible_virtualization_type']
    values[u'硬件型号'] = fact['ansible_product_name']
    values[u'序列号'] = fact['ansible_product_serial']
    values[u'IP地址'] = fact['ansible_all_ipv4_addresses']
    values[u'操作系统'] = fact['ansible_distribution'] +"_"+ fact['ansible_architecture'] +"_"+ fact['ansible_distribution_version']
    values[u'存储'] = fact['ansible_devices']
    values[u'文件系统'] = fact['ansible_mounts']
    values[u'网卡'] = {}
    for key in fact:
        if type(fact[key]) == dict:
            if fact[key].get('type') == 'ether' and fact[key].has_key('device') and fact[key].has_key('module'):
                values[u'网卡'][fact[key]['device']] = {'macaddress':fact[key]['macaddress'],'active':fact[key]['active']}
                if fact[key].has_key('module'): values[u'网卡'][fact[key]['device']]['module'] = fact[key]['module']
                if fact[key].has_key('speed'): values[u'网卡'][fact[key]['device']]['speed'] = fact[key]['speed']
                if fact[key].has_key('ipv4'): values[u'网卡'][fact[key]['device']]['ipaddress'] = fact[key]['ipv4']['address']
    values[u'网络'] = {}
    if 'ansible_bond0' in fact:
        values[u'网络']['bond0'] = fact['ansible_bond0']
    if 'ansible_bond1' in fact:
        values[u'网络']['bond1'] = fact['ansible_bond1']
    return values

def main():
    ansible_api = ansible_facts.AnsibleAPI('10.214.129.160','admin','admin')
    couchdb_api = CouchDB('10.214.160.113:5984','devtest','zhouwenjun','123456')
    hosts = couchdb_api.getids("/_design/server/_view/by_ip")
    ansible_api.gethosts()
    ansible_api.hosts = [host for host in ansible_api.hosts if host['name'] in hosts]
    ansible_api.getfacts()
    for host in ansible_api.facts:
        values = getcolume(ansible_api.facts[host])
        print host + ": ",
        print couchdb_api.updatadoc(host,values)

if __name__ == "__main__":
#    url = sys.argv[1]
    main()
