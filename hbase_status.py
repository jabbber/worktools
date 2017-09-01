#!/usr/bin/env python2
import urllib2
import re
import sys
import json

dump_url = "http://10.214.160.196:60010/dump"

f = urllib2.urlopen(dump_url)

hbase_dump = f.read().decode('utf-8')

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

regions = {'data':[]}
for row in region_status:
    name = row[:row.find(':')]
    data = row[row.find(': ')+1:]
    data = re.sub('([a-zA-Z]\w+)(?![=\w])','"\\1"',data)
    data = data.replace('"NaN"','None')
    item = eval("dict(%s)"%data)
    item['hostname'] = name
    for i in item.pop('coprocessors'):
        item['coprocessors'+'_'+i] = True
    regions['data'].append(item)

print json.dumps(regions,sort_keys=True,indent=4)


