#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
from bs4 import BeautifulSoup
for col in sys.argv[1:]:
    html = file(os.path.realpath(col),'r').read().decode('utf-8')

    soup = BeautifulSoup(html)
    #help(soup.body.div)
    for text in soup.body.div.findChildren():
        print text.getText(),
    print('')
