#!/usr/bin/env python
#author: zwj
#this script can join zypper pch and lu
import sys
import re
with open('pch.txt') as pchfile:
    pch = pchfile.read()
patchnames = {}
for line in pch.split("\n")[4:]:
    if re.match("^\s*$",line):
        continue
    patchname = re.findall("^[\w-]+\s+\|\s+\w+-((?:\w+-)*[a-zA-Z]\w+)(?:-\d\w*)*-\d+\s+\|", line)
    if len(patchname) == 1:
        if patchname[0]:
            #print patchname[0]
    	    patchnames[patchname[0]] = line
            continue
    sys.stderr.write("This line in 'pch' can not match:\n'>>'%s\n"%line)

with open('lu.txt') as lufile:
    lu = lufile.read()
for line in lu.split("\n")[4:]:
    if re.match("^\s*$",line):
        continue
    updatename = re.findall("\S+\s+\|\s+[\w-]+\s+\|\s+((?:\w+-)*\w+)\s+\|", line)
    if len(updatename) == 1:
        if updatename[0]:
            #print updatename[0]
            if updatename[0] in patchnames:
                print line + patchnames[updatename[0]]
            continue
    sys.stderr.write("This line in 'pch' can not match:\n'>>'%s\n"%line)

