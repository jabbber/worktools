#!/usr/bin/env python2
## -*- coding: utf-8 -*-
import csv
import json
import os,sys
import commands
import re

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

def csvreader(filepath):
    with open(filepath) as f:
        content = f.read()
    tmpfile = '/tmp/tmpcsv-2bbecb7e-c8fa-4dda-9314-21584a5d6493'
    with open(tmpfile,'w') as f:
        content = re.sub('\r\n','\n',content)
        f.write(content)
    with open(tmpfile) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    os.unlink(tmpfile)
    return rows

if __name__ == "__main__":
    rows = csvreader(sys.argv[1])
    for doc in rows:
        print jsondump(doc) + ','
