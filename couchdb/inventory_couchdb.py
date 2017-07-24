#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#This is a inventory script for ansible ans ansible tower
#
# you must set the 
# "server_url"
# and 
# "select_by"
# in the environment variables first
#
#author: zhouwenjun
#version: 1.1.0
import os
import requests
import json

#select_by要搜索的属性名
select_key = u'机房区域'

#搜索结果的分组依据
group_key = u'应用项目'

os.environ["LC_ALL"] = "en_US.utf-8"

server_url = os.environ.get('server_url')
select_by = os.environ.get('select_by')
if not server_url or not select_by:
    exit(1)
if type(select_by) == str:
    select_by = unicode(select_by,encoding='utf-8')

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

req = {
    "selector": {
        select_key: {
            "$regex": select_by
        },
        u"主IP": {"$gt": None}
    },
    "fields": [u"主机名",u"主IP", group_key],
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
for doc in docs:
    result['_meta']['hostvars'][doc[u'主机名']] = {'ansible_host':doc[u'主IP']}
    if group_key not in doc:
        result['null'].append(doc[u'主机名'])
    elif doc[group_key] not in result:
        result[doc[group_key]] = [doc[u'主机名']]
    else:
        result[doc[group_key]].append(doc[u'主机名'])

if not result['_meta']['hostvars']:
    result['_meta']['hostvars']['error: "select_by" = "%s"'%select_by] = {}

print(jsondump(result))
