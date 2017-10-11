#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#This is a inventory script for ansible ans ansible tower
#
# you must set the 
# "server_url"
# in the environment variables first
#
#author: zhouwenjun
#version: 1.4.0
import os
import requests
import json
import re

#请求的couchdb数据库连接
server_url = os.environ.get('server_url',"http://ansible:tower@10.214.160.210:5984/beta")
#select_by要搜索的属性名
select_by = os.environ.get('select_by',u'.*')
select_key = os.environ.get('select_key',u'机房区域')
#搜索结果的分组依据
group_key = os.environ.get('group_key',u'机房区域/应用项目')


os.environ["LC_ALL"] = "en_US.utf-8"
os_blacklist = ['Esx','windows']

if not server_url:
    exit(1)

def decoder(i):
    if type(i) == str:
        if i.find('\u') > -1:
            i = i.decode('unicode-escape')
        else:
            i = i.decode('utf-8')
    return i

select_by = decoder(select_by)
select_key = decoder(select_key)
group_key = decoder(group_key)

group_keys = group_key.split('/')

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

def blacklist(word,keys):
    for key in keys:
        if re.match(key,word,flags=re.IGNORECASE):
            return True
    return False


req = {
    "selector": {
        select_key: {
            "$regex": select_by
        },
        u"主IP": {"$gt": None}
    },
    "fields": [u"主机名",u"主IP",u"操作系统"]+group_keys,
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
for doc in docs:
    if blacklist(doc.get(u'操作系统',''),os_blacklist):
        continue
    result['_meta']['hostvars'][doc[u'主机名']] = {'ansible_host':doc[u'主IP']}
    group_name = '/'.join([doc.get(key) or 'None' for key in group_keys])
    if group_name not in result:
        result[group_name] = [doc[u'主机名']]
    else:
        result[group_name].append(doc[u'主机名'])

if not result['_meta']['hostvars']:
    result['_meta']['hostvars']['error: "select_by" = "%s"'%select_by] = {}

print(jsondump(result))
