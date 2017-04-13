#!/usr/bin/env python2
## -*- coding: utf-8 -*-
import csv
import json
import sys
import commands

def jsondump(item):
    return json.dumps(item, sort_keys=True,indent=4).decode('unicode_escape').encode('utf-8')

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for doc in rows:
        print jsondump(doc) + ','
