#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from openpyxl.reader.excel import load_workbook

wb = load_workbook(filename = sys.argv[1])
sheet_ranges = wb.get_active_sheet()

def converthtml(sheet):
    if len(sys.argv) > 2:
        if sys.argv[2] == "html":
            html = True
        else:
            html = False
    else:
        html = False

    row = 0
    row_empty = 0
    row_max_empty = 10
    end = False
    output = ""
    if html:
        output += "<table border>\n"
    while not end:
        row += 1
        col = []
        col_empty = 0
        col_max_empty = 3
        col_end = False
        if html:
            output+= "  <tr>\n"
        while not col_end:
            value = sheet.cell(row=row,column=len(col)+1).value
            if value:
                value = value.encode('utf-8')
                col_empty = 0
            else:
                value = ''
                col_empty += 1
            col.append(value)
            if col_empty >= col_max_empty:
                col = col[:-col_max_empty]
                col_end = True
        if html:
            if len(col) > 0:
                output += '    <td>%s'%("</td>\n    <td>".join(col))
                row_empty = 0
            else:
                pass
                output += '    <td>%s'%("</td>\n    <td>".join(col))
                row_empty += 1
        else:
            print "%s"%value,
        if html:
            output += '</td>\n  </tr>\n'
        else:
            print ''
        if row_empty >= row_max_empty:
            end = True
    if html:
        output += '</table>\n'
    return output

print converthtml(sheet_ranges)
