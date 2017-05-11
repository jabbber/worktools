#!/usr/bin/env python2
## -*- coding: utf-8 -*-
import csv
import json
import os,sys
import requests
import re

debug = False

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

def csvreader(f):
    content = [row.rstrip() for row in f]
    reader = csv.DictReader(content)
    rows = list(reader)
    return rows

class CouchDB:
    def __init__(self,host,database,user,passwd,ssl=False,verify=False):
        self.host = host
        self.database = database
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
        if 200 <= status < 300:
            return json.loads(content)
        elif status in warning or warning == 'all':
            print >> sys.stderr, self.Error(status,content,url)
        else:
            raise self.Error(status,content,url)
    def request(self,method, url ,data = None,warning=()):
        fullurl = "http"
        if self.ssl:
            fullurl += 's'
        fullurl += "://%s/%s%s"%(self.host,self.database,url)
        r =  requests.request(method,fullurl,auth=(self.user,self.__passwd),verify = self.verify, data = data)
        return self.__returnHandle(r.status_code,r.content,fullurl,warning)
    def getdoc(self,id):
        return self.request("GET","/"+id)
    def putdoc(self,doc):
        current = self.getdoc(doc["主机名"])
        diff = False
        for key in doc.keys():
            if doc[key] == "":
                doc.pop(key)
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
            return self.request("PUT","/"+doc['主机名'], data=jsondump(doc) )
        else:
            return None

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        rows = csvreader(f)
#    url = 'http://admin:admin@10.214.160.113:5984/devtest'
    db =  CouchDB('10.214.160.113:5984','devtest','zhouwenjun','123456',ssl=False,verify=False)
    for doc in rows:
        if doc.get('主机名') != "":
            result = db.putdoc(doc)
            print doc['主机名']+ ':'+ jsondump(result)

