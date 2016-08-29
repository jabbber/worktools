#!/usr/bin/env python
#author: zwj
#this script can join zypper pch and pa
import sys
import re
with open('pch.txt') as pchfile:
    pch = pchfile.read()
patchnames = {}
for line in pch.split("\n")[4:]:
    if re.match("^\s*$",line):
        continue
    patchname = re.findall("^[\w-]+\s+\|\s+\w+-((?:[\w+]+-)*[a-zA-Z][\w+]+)(?:-\d\w*)*(?:-\d+)?\s+\|", line)
    if len(patchname) == 1:
        if patchname[0]:
            #print patchname[0]
    	    patchnames[patchname[0]] = line
            continue
    sys.stderr.write("This line in 'pch' can not match:\n'>>'%s\n"%line)

with open('pa.txt') as lufile:
    pa = pafile.read()
for line in pa.split("\n")[4:]:
    if re.match("^\s*$",line):
        continue
    updatename = re.findall(".+\s+\|\s+.+\s+\|\s+((?:[\w+]+-)*[\w+]+)\s+\|", line)
    if len(updatename) == 1:
        if updatename[0]:
            #print updatename[0]
            if updatename[0] in patchnames:
                print line + patchnames.pop(updatename[0])
            continue
    sys.stderr.write("This line in 'pa' can not match:\n'>>'%s\n"%line)

