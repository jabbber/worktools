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
    def __init__(self,url):
        self.url = url
    def __returnHandle(self,status,content):
        if debug:
            print status + ':' + content
        return json.loads(content)
    def getdoc(self,id):
        r = requests.get("%s/%s"%(self.url,id))
        return self.__returnHandle(r.status_code,r.content)
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
            r = requests.put("%s/%s"%(self.url,doc['主机名']), data=jsondump(doc) )
            return self.__returnHandle(r.status_code,r.content)
        else:
            return {"status":"skip", "reason":"No difference."}

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        rows = csvreader(f)
#    url = 'http://admin:admin@10.214.160.113:5984/devtest'
    url = sys.argv[2]
    for doc in rows:
        if '主机名' in doc:
            if doc['主机名'] != "":
                db = CouchDB(url)
                result = db.putdoc(doc)
                print doc['主机名']+ ':'+ jsondump(result)

