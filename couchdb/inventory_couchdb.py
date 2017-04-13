#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#This is a inventory script for ansible
#author: zhouwenjun
#version: 1.0.1

import requests
import json

#couchdb view api url
view_url = 'http://10.214.160.113:5984/devtest/_design/server/_view/by_ip?include_docs=true'
#分组的参考属性
group_key = '应用项目'

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

r = requests.get(view_url)

if r.status_code != 200:
    print(r.content)
    exit(1)

view = json.loads(r.content)
rows = view['rows']

result = {}
result['_meta'] = {'hostvars':{}}
result['null'] = []
group_key = group_key.decode('utf-8')
for row in rows:
    doc = row['doc']
    result['_meta']['hostvars'][row['key']] = {'hostname':row['id']}
    if group_key not in doc:
        result['null'].append(row['key'])
    elif doc[group_key] not in result:
        result[doc[group_key]] = [row['key']]
    else:
        result[doc[group_key]].append(row['key'])

print(jsondump(result))

