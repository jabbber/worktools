#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

col_names = ['机构代码','HostID','HostID说明','上线否','永久IP','其他IP','运行区域','OS类型','所在项目','允许单命令','允许日常检查','Agent端口','缺省版本','系统管理员1','系统管理员2','系统管理员3','坐标位置','系统级别','关联host','备注',]

project_alias = {
        '电子银行门户网站':{'项目管理: 门户网站','网银门户网站'},
        }

def parse(hostlist_file):
    with open(hostlist_file, encoding = 'cp936', newline = '\r\n') as org_hostlist_file:
        lines = [line.split('\t') for line in org_hostlist_file if line != '\r\n']
        host_info = {row[1]:{col_names[number]:row[number] for number in range(0,len(col_names))} for row in lines}
    return host_info

if __name__ == "__main__":
    host_info = parse(sys.argv[1])
#    print({value['所在项目'] for value in host_info.values()})
    key_set = set()
    for alias in project_alias.values():
        key_set.update(alias)

    hostlist = [value['HostID'] for value in host_info.values() if value['所在项目'] in key_set]
    hostlist.sort()
    for host in hostlist:
        print(host)
    print(len(hostlist))
