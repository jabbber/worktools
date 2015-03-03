#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import openimsi
from openimsi import TABLE_STYLE,TH_STYLE,TD_STYLE

def getTables(table_file,title):
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
    html = '<table width=%d %s>\n'%(total_width*PER,TABLE_STYLE)
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
                html += "<th width=%d %s>%s</th>"%(width*PER,TH_STYLE,val)
            html += '  </tr>\n'
        else:
            if tuple(row[1:3]) in filter_set:
                html += '  <tr>\n'
                for val in row:
                    html += "<td %s>%s</td>"%(TD_STYLE,val)
                html += '  </tr>\n'
            else:
                pass
    html += '</table>'
    return html

def table2htmlHighlight(table,filter_set):
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
    html = '<table width=%d %s>\n'%(total_width*PER,TABLE_STYLE)
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
                html += "<th width=%d %s>%s</th>"%(width*PER,TH_STYLE,val)
            html += '  </tr>\n'
        else:
            if tuple(row[1:3]) in filter_set:
                html += "  <tr bgcolor='yellow' >\n"
            else:
                html += '  <tr>\n'
            for val in row:
                html += "<td %s>%s</td>"%(TD_STYLE,val)
            html += '  </tr>\n'
    html += '</table>'
    return html


def openimsiDiff(file1, file2):
    title = '分区日常检查异常明细-未备注/未处理'
    table1 = getTables(file1,title)
    table2 = getTables(file2,title)
    return table2html(table1, genDiffSet(table1,table2))

if __name__ == '__main__':
    FILE1 = sys.argv[1]
    FILE2 = sys.argv[2]
    title = '分区日常检查异常明细-未备注/未处理'
    table1 = getTables(FILE1,title)
    table2 = getTables(FILE2,title)
    print table2html(table1, genDiffSet(table1,table2))

