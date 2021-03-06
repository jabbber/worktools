#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#This is a inventory script for ansible ans ansible tower
#
# you must set the 
# "server_url"
# in the environment variables first
#
#author: zhouwenjun
#version: 1.5.1
import os
import requests
import json
import re

#请求的couchdb数据库连接
server_url = os.environ.get('server_url',"https://ansible:ansible@10.214.129.248:6984/cmdb")
#select_by要搜索的属性名
select_by = os.environ.get('select_by',u'.*')
select_key = os.environ.get('select_key',u'机房区域')
#搜索结果的分组依据
group_key = os.environ.get('group_key',u'机房区域/应用项目/部署角色')


os.environ["LC_ALL"] = "en_US.utf-8"
os_blacklist = ['esx','windows']

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
        if re.search(key,word,flags=re.IGNORECASE):
            return True
    return False

req = {
    "selector": {
        select_key: {
            "$regex": select_by
        },
        u"IP": {"$gt": None}
    },
    "fields": [u"主机名",u"IP",u"ssh端口",u"操作系统",u"激活"]+group_keys,
    "limit": 9999,
}

r = requests.post(server_url+'/_find',json=req,verify=False)

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
    if doc.get(u'激活') == False:
        print '========',doc[u'主机名']
        continue
    result['_meta']['hostvars'][doc[u'主机名']] = {'ansible_host':doc[u'IP']}
    if doc.get(u'ssh端口'):
        result['_meta']['hostvars'][doc[u'主机名']]['ansible_port'] = doc.get(u'ssh端口')
    group_name = '/'.join([doc.get(key) or 'None' for key in group_keys])
    if group_name not in result:
        result[group_name] = [doc[u'主机名']]
    else:
        result[group_name].append(doc[u'主机名'])

if not result['_meta']['hostvars']:
    result['_meta']['hostvars']['error: "select_by" = "%s"'%select_by] = {}

print(jsondump(result))

