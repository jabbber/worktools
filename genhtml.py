#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import openimsi

HOST_LIST = 'hostlist.xlsx'
BLACK_LIST = None
SAVE_DIR = './target/'

for file_name in sys.argv[1:]:
    name = file_name.split('/')[-1]
    name = '.'.join(name.split('.')[:-1])
    print "convert %s ..."%name
    open('%s%s.html'%(SAVE_DIR,name),'w').write(openimsi.get_html(file_name,'all',HOST_LIST,BLACK_LIST))
    
