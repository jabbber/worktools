#!/usr/bin/env python
from __future__ import print_function
import os
import sys
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

tmp = {}
size = os.path.getsize(stracefile)

print('parse...',file=sys.stderr)
with open(stracefile) as stracef:
    line = True
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
        if stracef.tell()%100000 == 0:
            print('%d'%stracef.tell(),end='\r',file=sys.stderr)
print('\nfinished!',file=sys.stderr)

