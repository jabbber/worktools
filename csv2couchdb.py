#!/usr/bin/env python2
## -*- coding: utf-8 -*-
import csv
import json
import sys
import commands

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

class CouchDB:
    def __init__(self,url):
        self.url = url
        self.cmd = "curl -s -X"
    def __returnHandle(self,a,b):
        if a == 0:
            return json.loads(b)
        else:
            return {}
    def getdoc(self,id):
        a,b = commands.getstatusoutput("%s GET %s/%s"%(self.cmd,self.url,id))
        return self.__returnHandle(a,b)
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
            elif doc[key] != current[key.decode('utf-8')].encode('utf-8'):
                diff = True
                break
        for key in current:
            if key != "_rev" and key !="_id" and key.encode('utf-8') not in doc:
                diff = True
                print 3
                print key
                break
        if diff:
            if "_rev" in current:
                doc['_rev'] = current['_rev']
            a,b = commands.getstatusoutput("%s PUT %s/%s -d '%s'"%(self.cmd,self.url,doc['主机名'],jsondump(doc)))
            return self.__returnHandle(a,b)
        else:
            return {"status":"skip", "reason":"No difference."}

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

#    url = 'http://admin:admin@10.214.160.113:5984/devtest'
    url = sys.argv[2]
    for doc in rows:
        if '主机名' in doc:
            if doc['主机名'] != "":
                db = CouchDB(url)
                result = db.putdoc(doc)
                print doc['主机名']+ ':'+ jsondump(result)

