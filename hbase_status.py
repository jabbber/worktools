#!/usr/bin/env python2
import urllib2
import re
import os,sys,time
import json

dump_url = "http://10.214.128.51:60010/dump"

cache_file = '/tmp/hbase_dump_cache'
cache_timeout = 60
cache = True

if os.path.exists(cache_file):
    if time.time() - os.stat(cache_file).st_mtime > cache_timeout:
        f = urllib2.urlopen(dump_url)
    else:
        cache = False
        f = open(cache_file)
else:
    f = urllib2.urlopen(dump_url)
hbase_dump = f.read().decode('utf-8')
f.close()

if cache:
    with open(cache_file,'w') as cache:
        cache.write(hbase_dump.encode('utf-8'))

if not hbase_dump:
    exit(1)

def sectionCut(text,name):
    section = re.findall('''
        %s:\\n
        =+\\n
        (.+?)
        \\n{2,}
        .+:\\n
        =+
        '''%name,text,flags=re.VERBOSE+re.DOTALL)
    if len(section) == 1:
        return section[0]
    else:
        sys.stderr.write('"Servers" sections cannot find!\n')
        exit(2)

region_status = sectionCut(hbase_dump,'Servers').split('\n')

original_data={}

regions = {'data':[]}
for row in region_status:
    name = row[:row.find(':')].split(',')[0]
    data = row[row.find(': ')+1:]
    data = re.sub('([a-zA-Z]\w+)(?![=\w])','"\\1"',data)
    data = data.replace('"NaN"','None')
    item = eval("dict(%s)"%data)
    for key in item.keys():
        item['{#%s}'%key.upper()] = item.pop(key)
    item['{#HOSTNAME}'] = name
    for i in item.pop('{#COPROCESSORS}'):
        item['{#COPROCESSORS'+'_'+i.upper()+'}'] = True
    regions['data'].append(item)
    original_data[name] = item

if len(sys.argv) == 2 and sys.argv[1] == 'discovery':
    print json.dumps(regions,sort_keys=True,indent=4)
elif len(sys.argv) == 3:
    if original_data.get(sys.argv[1]):
        print original_data.get(sys.argv[1]).get(sys.argv[2])
else:
    print json.dumps(regions,sort_keys=True,indent=4)

