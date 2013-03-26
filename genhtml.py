#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import openimsi

HOST_LIST = 'hostlist.xlsx'
BLACK_LIST = None
SAVE_DIR = './target/'

def convert(file_name, output_file, out_type = 'html'):
    t = openimsi.Tables()
    t.hostlist = t.load_list(HOST_LIST)
    t.blacklist = t.load_list(BLACK_LIST)
    t.load(file_name)
    if out_type == 'html':
        open(output_file + '.html', 'w').write(t.get_html('all'))
    elif out_type == 'xlsx':
        t.get_xlsx(output_file +'.xlsx')

if __name__ == '__main__':
    for file_name in sys.argv[1:]:
        name = file_name.split('/')[-1]
        name = '.'.join(name.split('.')[:-1])
        print "convert %s"%name
        output_file = '%s%s'%(SAVE_DIR,name)
        convert(file_name,output_file,'xlsx')
    print 'Convert Complite!'
    sys.exit(0)

