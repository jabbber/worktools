#!/usr/bin/env python2
# split the strace -f output by process/task id
from __future__ import print_function
import os
import sys
import time
import threading

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
            time.sleep(0.2)
        print('100%',end='\r',file=sys.stderr)
        print('\nfinished!',file=sys.stderr)

def main ():
    tmp = {}
    size = os.path.getsize(stracefile)
    with open(stracefile) as stracef:
        line = True
        myProgress = Progress(stracef,size)
        myProgress.start()
        #while line:
        #    line = stracef.readline()
        for line in stracef:
            try:
                tid = int(line[:line.index(' ')])
            except:
                continue
            if tid in tmp:
                pass
            else:
                tmp[tid] = open(os.path.join(outputdir,os.path.basename(stracefile)+'.'+str(tid)),'w')
            tmp[tid].write(line)

if __name__ == "__main__":
    debug = False
    if debug:
        import cProfile as profile
        profile.run("main()")
    else:
        main()

