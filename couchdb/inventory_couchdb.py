#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#This is a inventory script for ansible ans ansible tower
#
# you can set the "server_url" and "select_by" in the environment variables
#
#author: zhouwenjun
#version: 1.1.0
import os
import requests
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--server_url")
parser.add_argument("--select_by")
args = parser.parse_args()

server_url = args.server_url or os.environ.get('server_url')
select_by = args.select_by or os.environ.get('select_by')
if not server_url and select_by:
    parser.print_usage()
    exit(1)
if type(select_by) == str:
    select_by = unicode(select_by,encoding='utf-8')

#分组的参考属性

group_key = u'应用项目'

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

req = {
    "selector": {
        u"分类": {
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
