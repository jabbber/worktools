#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os,sys
import time
from bs4 import BeautifulSoup
result={}
n = 0
for col in sys.argv[2:]:
    n += 1
    print "\rparse %s/%s ... %s" % (n,len(sys.argv[2:]),col),
    html = open(os.path.realpath(col),'r').read()
    try:
        html = html.decode('utf-8')
    except:
        html = html.decode('gbk')
    soup = BeautifulSoup(html)
    #help(soup.body.div)
    hostname,ip = soup.body.div.findChildren()
    hostname = str(hostname.string.encode('utf-8'))
    ip = str(ip.get_text().encode('utf-8'))
    result[hostname] = {}
    result[hostname]['ip'] = ip
    checklist = soup.body.table.find_all('tr')
    del checklist[0]
    if sys.argv[1] != "系统网络状态":
        for item in checklist[:15]+checklist[17:]:
            temp = item.find_all('td')
            checkname = str(temp[-3].div.string.encode('utf-8'))
            checklog = str(temp[-1].get_text().encode('utf-8'))
            result[hostname][checkname] = checklog
    else:
        for item in checklist[15:17]:
            temp = item.find_all('td')
            checkname = str(temp[-2].div.string.encode('utf-8'))
            checklog = str(temp[-1].get_text().encode('utf-8'))
            if checklog.find('\r') < 0:
                values = []
                for line in checklog.split('\n'):
                    if line:
                        values.append(line)
            else:
                values = checklog.split('\r\n\r\n')
            if len(values) != 8:
                pass
            else:
                interfacename1 = 'eth' + values[0][values[0].find('eth')+3]
                interfacename2 = 'eth' + values[4][values[4].find('eth')+3]
                interfacestat1 = values[1][12:]
                interfacestat2 = values[5][12:]
                result[hostname][checkname] = [interfacename1,interfacestat1,interfacename2,interfacestat2]
print '\r                                                                                                                                  '
checkname = str(sys.argv[1])
if checkname == 'ip':
    for hostname in sorted(result.keys()):
        print hostname + " " + result[hostname]['ip']
elif checkname != '系统网络状态':
    normalvalue = '正常'
    output = {}
    for hostname in sorted(result.keys()):
        try:
            result[hostname][checkname]
        except:
            print "没有正确解析:"
            print "\n"+ hostname + '\t'+ checkname
        if result[hostname][checkname].find(normalvalue) > -1:
            pass
        else:
            abnormal = result[hostname][checkname]
            if abnormal == None:
                pass
            else:
                for item in abnormal.split('\n'):
                    if item in ("","\r","\n"):
                        pass
                    else:
                        if item.find("end_request: I/O error") > 0:
                            item = "end_request: I/O error"
                        elif item.find("Log statistics;") > 0:
                            item = "syslog-ng[xxx]: Log statistics;"
                        elif item.find("sshd[") > 0:
                            item = "sshd[xxx]: error"
                        elif checkname == '文件系统是否需要fsck':
                            if item.find("Last checked:") > 0:
                                if item[-1] != "\n":
                                    time_str = item[-24:]
                                else:
                                    time_str = item[-25:-1]
                                time_sec = time.mktime(time.strptime(time_str))
                                time_ = time.time() - time_sec
                                if time_ < 15552000:
                                    item = "小于180天"
                                else:
                                    item = "大于180天"
                        if output.has_key(item):
                            if hostname in output[item]:
                                pass
                            else:
                                output[item].append(hostname)
                        else:
                            output[item] = [hostname]
    print "%s:\n"%checkname
    for abnormal in output:
        if abnormal in ("","\r"):
            pass
        else:
            print "问题主机:"
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

