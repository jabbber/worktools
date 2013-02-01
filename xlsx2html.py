#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import readxlsx

for xlsx in sys.argv[1:]:
    name = xlsx.split('/')[-1]
    print "convert %s ..."%name
    open('%s.html'%name,'w+').write(readxlsx.xlsx2html(xlsx))
    
