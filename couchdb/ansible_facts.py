#!/usr/bin/env python2
## -*- coding: utf-8 -*-
import json
import os,sys
import requests
import time

debug = False

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

class AnsibleAPI:
    def __init__(self,host,user,passwd):
        self.host = host
        self.user = user
        self.__passwd = passwd
        self.ssl = True
        self.verify = False
    class Error(Exception):
        def __init__(self, status,content,url):
            self.status = status
            self.content = content
            self.url = url
        def __str__(self):
            return repr("%d : '%s' url='%s'"%(self.status,self.content,self.url))
    def __returnHandle(self,status,content,url):
        if status == 200:
            return json.loads(content)
        else:
            raise self.Error(status,content,url)
    def request(self,method, url ,data = None):
        fullurl = "http"
        if self.ssl:
            fullurl += 's'
        fullurl += "://%s%s"%(self.host,url)
        if "?" in fullurl:
            fullurl += "&format=json"
        else:
            fullurl += "?format=json"
        if data:
            r =  requests.request(method,fullurl,auth=(self.user,self.__passwd),verify = self.verify, data = data)
        else:
            r =  requests.request(method,fullurl,auth=(self.user,self.__passwd),verify = self.verify)
        return self.__returnHandle(r.status_code,r.content,fullurl)
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
        result = self.request("GET","/api/v1/hosts/%d/job_events/?page=last"%hostid)
        jobs = result['results']
        for job in jobs:
            if job['event_data']['res'].has_key('ansible_facts'):
                return job['event_data']['res']['ansible_facts']
        while result['previous']:
            result = self.request("GET",result['previous'])
            jobs = result['results']
            for job in jobs:
                if job['event_data']['res'].has_key('ansible_facts'):
                    return job['event_data']['res']['ansible_facts']
        return None
    def getfacts(self):
        self.gethosts()
        facts = {}
        for host in self.hosts:
            print "%s %s %s"%(host['id'] ,host['name'],time.ctime())
            try:

                fact =  self.getfactsbyhostid(host['id'])
            except self.Error, content:
                print >> sys.stderr, content
            if fact:
                facts[host['name']] = fact
        return facts

if __name__ == "__main__":
#    url = 'https://10.214.129.160/api/v1/hosts/?format=json'
    pass
