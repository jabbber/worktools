#!/usr/bin/env python2
## -*- coding: utf-8 -*-
import json
import os,sys
import requests
import time
import multiprocessing.dummy

debug = False

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

class AnsibleAPI:
    def __init__(self,host,user,passwd,ssl=True,verify=False):
        self.host = host
        self.user = user
        self.__passwd = passwd
        self.ssl = ssl
        self.verify = verify
    class Error(Exception):
        def __init__(self, status,content,url):
            self.status = status
            self.content = content
            self.url = url
        def __str__(self):
            return repr("%d : '%s' url='%s'"%(self.status,self.content,self.url))
    def __returnHandle(self,status,content,url,warning=()):
        if status == 200:
            return json.loads(content)
        elif status in warning or warning == 'all':
            print >> sys.stderr, self.Error(status,content,url)
        else:
            raise self.Error(status,content,url)
    def request(self,method, url ,data = None,warning=()):
        fullurl = "http"
        if self.ssl:
            fullurl += 's'
        fullurl += "://%s%s"%(self.host,url)
        if "?" in fullurl:
            fullurl += "&format=json"
        else:
            fullurl += "?format=json"
        r =  requests.request(method,fullurl,auth=(self.user,self.__passwd),verify = self.verify, data = data)
        return self.__returnHandle(r.status_code,r.content,fullurl,warning)
    def gethosts(self):
        result = self.request("GET","/api/v1/hosts/")
        count = result['count']
        hosts = result['results']
        while result['next']:
            result = self.request("GET",result['next'])
            hosts.extend(result['results'])
        if len(hosts) != count:
            print >> sys.stderr, 'count = %d but actually count is %d'%(count,len(hosts))
        self.hosts = hosts
        return hosts
    def getfactsbyhostid(self,hostid):
        def getfactsin(hostid,events):
            warning = 'all'
            result = self.request("GET","/api/v1/hosts/%d/%s/?page=last"%(hostid,events),warning=warning)
            if not result:
                return None
            jobs = result.get('results')
            for job in jobs:
                if job['event_data']['res'].has_key('ansible_facts'):
                    return job['event_data']['res']['ansible_facts']
            while result['previous']:
                result = self.request("GET",result['previous'],warning=warning)
                jobs = result['results']
                for job in jobs:
                    if job['event_data']['res'].has_key('ansible_facts'):
                        return job['event_data']['res']['ansible_facts']
            return None
        job_fact = getfactsin(hostid,'job_events')
        command_fact = getfactsin(hostid,'ad_hoc_command_events')
        return job_fact or command_fact
    def getfacts(self):
        pool = multiprocessing.dummy.Pool(50)
        results = pool.map(self.getfactsbyhostid,[host['id'] for host in self.hosts])
        facts = dict(zip([host['name'] for host in self.hosts],results))
        for host in facts.keys():
            if not facts[host]:
                facts.pop(host)
        self.facts = facts
        return facts

def main():
    api = AnsibleAPI('10.214.129.160','admin','admin')
    api.gethosts()
    print time.ctime()
    api.getfacts()
    print time.ctime()
    print len(api.hosts)
    print len(api.facts)
    print api.facts.keys()
    return api
if __name__ == "__main__":
#    url = 'https://10.214.129.160/api/v1/hosts/?format=json'
    pass
