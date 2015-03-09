#!/usr/bin/env python2
# split the strace -f output by process/task id
from __future__ import print_function
import os
import sys
from time import sleep
import threading
import re
from datetime import datetime, timedelta

if len(sys.argv) != 3:
    print("usage:")
    print("{} SOURCE_FILE DES_DIR".format(sys.argv[0]))
    exit()

stracefile=sys.argv[1]
outputdir=sys.argv[2]

if not os.path.isfile(stracefile):
    print("'{}' is not a file!".format(stracefile))
    sys.exit(1)
if not os.path.isdir(outputdir):
    print("'{}' is not a directory!".format(outputdir))
    sys.exit(2)

class Progress (threading.Thread):
    def __init__(self, fd, fsize):
        threading.Thread.__init__(self)
        self.fd = fd 
        self.fsize = fsize//100
    def run(self):
        print('parse...',file=sys.stderr)
        while not self.fd.closed:
            print('{}%'.format(self.fd.tell()//self.fsize),end='\r',file=sys.stderr)
            sleep(0.2)
        print('100%',end='\r',file=sys.stderr)
        print('\nfinished!',file=sys.stderr)

def main ():
    cs_list = dict()
    ss_list = dict()
    sql_list = dict()
    cs_req_num = 0
    cs_req_time = timedelta(0)
    ss_req_num = 0
    ss_req_time = timedelta(0)
    sql_req_num = 0
    sql_req_time = timedelta(0)

    fd_dict = {}
    size = os.path.getsize(stracefile)
    tid_unfinish = {}
    fd_filter = re.compile('\s+([\d:\.]+)\s+(recvfrom|writev|sendto|read|getpeername|close)\((\d+),')
    method_filter = re.compile('"(POST|HTTP)')
    with open(stracefile) as stracef:
        line = True
        myProgress = Progress(stracef,size)
        myProgress.start()
        for line in stracef:
            try:
                tid = int(line[:line.index(' ')])
            except:
                continue
            if tid in tid_unfinish:
                time, func, fd = tid_unfinish.pop(tid)
            else:
                fd_res = fd_filter.search(line)
                if not fd_res:
                    continue
                time, func, fd = fd_res.groups()
                if not fd in fd_dict:
                    fd_dict[fd] = open(os.path.join(outputdir,os.path.basename(stracefile)+'.fd'+str(fd)),'w')
                if line.find('<unfinished ...>'):
                    tid_unfinish[tid] = (time,func,fd)
                    fd_dict[fd].write(line)
                    continue
            fd_dict[fd].write(line)
            method_res = method_filter.search(line)
            if method_res:
                method = method_res.groups()[0]

            t = datetime.strptime(time,"%H:%M:%S.%f")
            if func == "writev" and method == "POST":
                if not fd in cs_list:
                    cs_list[fd] = t
            elif func == "recvfrom" and method == "HTTP" :
                if fd in cs_list:
                    cs_req_num += 1
                    cs_req_time += t-cs_list.pop(fd)
            elif func == "recvfrom" and method == "POST":
                if not fd in ss_list:
                    ss_list[fd] = t
            elif func == "writev" and method == "HTTP":
                if fd in ss_list:
                    ss_req_num += 1
                    ss_req_time += t-ss_list.pop(fd)
            elif func == "sendto" :
                if not fd in sql_list:
                    sql_list[fd] = t
            elif func == "read" :
                if fd in sql_list:
                    sql_req_num += 1
                    sql_req_time += t-sql_list.pop(fd)
            else:
                pass

    print("client req={},server req={},sql req={}".format(cs_req_num,ss_req_num,sql_req_num))
    if cs_req_num > 0 :
        cs_avg_time = (cs_req_time/cs_req_num).total_seconds()
        print("cs_avg_time={0}".format(cs_avg_time))
    if ss_req_num > 0 :
        ss_avg_time = (ss_req_time/ss_req_num).total_seconds()
        print("ss_avg_time={0}".format(ss_avg_time))
    if sql_req_num > 0 :
        sql_avg_time = (sql_req_time/sql_req_num).total_seconds()
        print("sql_avg_time={0}".format(sql_avg_time))

if __name__ == "__main__":
    debug = False
    if debug:
        import cProfile as profile
        profile.run("main()")
    else:
        main()

