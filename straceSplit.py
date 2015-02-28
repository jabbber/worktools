#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import time
import threading

if len(sys.argv) != 3:
    print("usage:")
    print("%s SOURCE_FILE DES_DIR"%sys.argv[0])
    exit()

stracefile=sys.argv[1]
outputdir=sys.argv[2]

if not os.path.isfile(stracefile):
    print("'%s' is not a file!"%stracefile)
    sys.exit(1)
if not os.path.isdir(outputdir):
    print("'%s' is not a directory!"%outputdir)
    sys.exit(2)

class Progress (threading.Thread):
    def __init__(self, fd, fsize):
        threading.Thread.__init__(self)
        self.fd = fd 
        self.fsize = fsize//100
    def run(self):
        while not self.fd.closed:
            print('{}%'.format(self.fd.tell()//self.fsize),end='\r',file=sys.stderr)
            time.sleep(1)

tmp = {}
size = os.path.getsize(stracefile)

print('parse...',file=sys.stderr)
with open(stracefile) as stracef:
    line = True
    myProgress = Progress(stracef,size)
    myProgress.start()
    while line:
        line = stracef.readline()
        try:
            tid = int(line[:line.find(' ')])
        except:
            continue
        if tmp.get(tid):
            pass
        else:
            tmp[tid] = open(os.path.join(outputdir,os.path.basename(stracefile)+'.'+str(tid)),'w')
        tmp[tid].write(line)
print('\nfinished!',file=sys.stderr)

