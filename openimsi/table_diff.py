#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import openimsi


def getTables(table_file):
    tables = openimsi.Tables()
    tables.load(table_file)
    for i,value in enumerate(tables.titles):
        if value == title:
            break
    return tables.tables[i]

def genDiffSet(table1,table2):
    getDiffKey = lambda table:{tuple(row[1:3]) for row in table}
    diffkey1 = getDiffKey(table1)
    diffkey2 = getDiffKey(table2)

    return diffkey1.difference(diffkey2)

def table2html(table,filter_set):
    column_widths = []
    PER = 10
    MIN_WIDTH = 2
    MAX_WIDTH = 50
    for row in table:
        for i, value in enumerate(row):
            if type(value) == str:
                l = len(value.decode('utf-8'))
                if l == len(value):
                    l = l/2 + 1
            elif type(value) == int:
                l = len(str(value))
            else:
                l = len(value)
            if len(column_widths) > i:
                if l > column_widths[i]:
                        column_widths[i] = l
            else:
                column_widths.append(l)
    total_width = 0
    for width in column_widths:
        if width < MAX_WIDTH:
            total_width += width
        else:
            total_width += MAX_WIDTH
    tablestyle = "width=%s style='BORDER-BOTTOM-STYLE: solid; BORDER-RIGHT-STYLE: solid; BORDER-TOP-STYLE: solid; BORDER-LEFT-STYLE: solid' border=1 cellSpacing=0 borderColor=#000000 cellPadding=1 bgColor=#ffffff"%(total_width*PER)
    tdstyle = 'style="white-space:nowrap"'
    html = '<table %s>\n'%tablestyle
    for row in table:
        if row[0] == '序号':
            html += '  <tr>\n'
            for i, val in enumerate(row):
                if column_widths[i] < MIN_WIDTH:
                    width = MIN_WIDTH
                elif column_widths[i] > MAX_WIDTH:
                    width = MAX_WIDTH
                else:
                    width = column_widths[i]
                html += "<td width=%s ><NOBR><FONT size=2 face=宋体 color=#0909f7><STRONG>%s</STRONG></FONT></NOBR></td>"%(width*PER,val)
            html += '  </tr>\n'
        else:
            if tuple(row[1:3]) in filter_set:
                html += '  <tr>\n'
                for val in row:
                    html += "<td style='word-break:break-all' ><FONT size=2 face=宋体  >%s</FONT></td>"%val
                html += '  </tr>\n'
            else:
                pass
    html += '</table>'
    return html

if __name__ == '__main__':
    FILE1 = sys.argv[1]
    FILE2 = sys.argv[2]
    title = '分区日常检查异常明细-未备注/未处理'
    table1 = getTables(FILE1)
    table2 = getTables(FILE2)
    print table2html(table1, genDiffSet(table1,table2))
