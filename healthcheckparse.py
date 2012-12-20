#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
from bs4 import BeautifulSoup
result={}
for col in sys.argv[1:]:
    print "parse %s" % col
    html = file(os.path.realpath(col),'r').read().decode('utf-8')

    soup = BeautifulSoup(html)
    #help(soup.body.div)
    hostname,ip = soup.body.div.findChildren()
    hostname = hostname.string.encode('utf-8')
    try:
        ip = ip.string.encode('utf-8')
    except:
        ip = ip.string
    result[hostname] = {}
    result[hostname]['ip'] = ip
    checklist = soup.body.table.find_all('tr')
    del checklist[0]
#    print checklist[15:17]
    for item in checklist[:15]+checklist[17:]:
        temp = item.find_all('td')
        checkname = temp[-3].div.string.encode('utf-8')
        try:
            checklog = temp[-1].div.string.encode('utf-8')
        except:
            checklog = temp[-1].div.string
        result[hostname][checkname] = checklog

checkname = '检查引导日志'
normalvalue = '正常'
output = {}
for hostname in sorted(result.keys()):
    if result[hostname][checkname] == normalvalue:
        pass
    else:
        abnormal = result[hostname][checkname]
        for item in abnormal.split('\n'):
            if output.has_key(item):
                if hostname in output[item]:
                    pass
                else:
                    output[item].append(hostname)
            else:
                output[item] = [hostname]
print "%s:"%checkname
for abnormal in output:
    if abnormal == "":
        pass
    else:
        print "hostlist:"
        for hostname in output[abnormal]:
            print hostname
        print "result:\n" + abnormal

