#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#This is a inventory script for ansible ans ansible tower
#
# you can set the server_url and label in the environment variables
#
#author: zhouwenjun
#version: 1.1.0
import os
import requests
import json

server_url = os.environ.get('server_url')
label = os.environ.get('label')
if not server_url:
#couchdb view api url
    server_url = 'http://zhouwenjun:123456@10.214.160.210:5984/devtest'
if not label:
    label = '生产区服务器'
#分组的参考属性

group_key = '应用项目'

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

req = {
    "selector": {
        "分类": {
            "$regex": label
        },
        "主IP": {"$gt": None}
    },
    "fields": ["主机名","主IP", group_key],
    "limit": 9999,
}

r = requests.post(server_url+'/_find',json=req)

if r.status_code != 200:
    print(r.content)
    exit(1)

view = json.loads(r.content)
docs = view['docs']

result = {}
result['_meta'] = {'hostvars':{}}
result['null'] = []
group_key = group_key.decode('utf-8')
for doc in docs:
    result['_meta']['hostvars'][doc[u'主机名']] = {'ansible_host':doc[u'主IP']}
    if group_key not in doc:
        result['null'].append(doc[u'主机名'])
    elif doc[group_key] not in result:
        result[doc[group_key]] = [doc[u'主机名']]
    else:
        result[doc[group_key]].append(doc[u'主机名'])

print(jsondump(result))
