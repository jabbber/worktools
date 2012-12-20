#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
from bs4 import BeautifulSoup
result={}
for col in sys.argv[2:]:
    print "parse %s" % col
    html = file(os.path.realpath(col),'r').read().decode('utf-8')

    soup = BeautifulSoup(html)
    #help(soup.body.div)
    hostname,ip = soup.body.div.findChildren()
    hostname = hostname.string.encode('utf-8')
    ip = ip.get_text().encode('utf-8')
    result[hostname] = {}
    result[hostname]['ip'] = ip
    checklist = soup.body.table.find_all('tr')
    del checklist[0]
#    print checklist[15:17]
    for item in checklist[:15]+checklist[17:]:
        temp = item.find_all('td')
        checkname = temp[-3].div.string.encode('utf-8')
        checklog = temp[-1].get_text().encode('utf-8')
        result[hostname][checkname] = checklog
checkname = sys.argv[1]
normalvalue = '正常'
output = {}
for hostname in sorted(result.keys()):
    if result[hostname][checkname] == normalvalue:
        pass
    else:
        abnormal = result[hostname][checkname]
        if abnormal == None:
            pass
        else:
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
        print "问题节点:"
        for hostname in output[abnormal]:
            print hostname
        print "信息结果:\n" + abnormal + "\n"

