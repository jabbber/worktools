#!/usr/bin/env python2
import csv
import json
import sys

with open(sys.argv[1]) as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for row in rows:
    a = json.dumps(row, sort_keys=True,indent=4)
    print a.decode('unicode_escape').encode('utf-8') + ','
