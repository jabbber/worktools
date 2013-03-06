#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os,sys
from bs4 import BeautifulSoup
result={}
n = 0
for col in sys.argv[2:]:
    n += 1
    print "\rparse %s/%s ... %s" % (n,len(sys.argv[2:]),col),
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
    if sys.argv[1] != "系统网络状态":
        for item in checklist[:15]+checklist[17:]:
            temp = item.find_all('td')
            checkname = temp[-3].div.string.encode('utf-8')
            checklog = temp[-1].get_text().encode('utf-8')
            result[hostname][checkname] = checklog
    else:
        for item in checklist[15:17]:
            temp = item.find_all('td')
            checkname = temp[-2].div.string.encode('utf-8')
            checklog = temp[-1].get_text().encode('utf-8')
            values = checklog.split('\r\n\r\n')
            if len(values) != 7:
                pass
            else:
                interfacename1 = 'eth' + values[0][values[0].find('eth')+3]
                interfacename2 = 'eth' + values[3][values[3].find('eth')+3]
                interfacestat1 = values[1][12:]
                interfacestat2 = values[4][12:]
                result[hostname][checkname] = [interfacename1,interfacestat1,interfacename2,interfacestat2]
print '\r                                                                                                                                  '
checkname = sys.argv[1]
if checkname != '系统网络状态':
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
                for item in [abnormal]:#.split('\n'):
                    if output.has_key(item):
                        if hostname in output[item]:
                            pass
                        else:
                            output[item].append(hostname)
                    else:
                        output[item] = [hostname]
    print "%s:\n"%checkname
    for abnormal in output:
        if abnormal == "":
            pass
        else:
            print "问题分区名:"
            for hostname in output[abnormal]:
                print hostname
            if len(abnormal) <= 1000:
                print "信息结果:\n" + abnormal + "\n"
            else:
                print "信息结果:\n" + abnormal[:1000] + "...(请打开文件查看完整信息)" + "\n"
else:
    print "%s:\n"%checkname
    for hostname in sorted(result.keys()):
        for bondname in result[hostname]:
            if bondname.find('bond') < 0:
                pass
            else:
                if result[hostname][bondname][1] == 'up' and result[hostname][bondname][3] == 'up':
                    pass
                elif result[hostname][bondname][1] != 'up' and result[hostname][bondname][3] != 'up':
                    print "%s %s的%s，%s断开"%(hostname,bondname,result[hostname][bondname][0],result[hostname][bondname][2])
                elif result[hostname][bondname][1] != 'up':
                    print "%s %s的%s断开"%(hostname,bondname,result[hostname][bondname][0])
                elif result[hostname][bondname][3] != 'up':
                    print "%s %s的%s断开"%(hostname,bondname,result[hostname][bondname][2])
                else:
                    print "%s 异常"%hostname

