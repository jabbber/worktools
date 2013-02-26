#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
from openpyxl.reader.excel import load_workbook

def table2html(table):
    tablestyle = 'border="1" style="border-collapse:collapse"'
    tdstyle = 'style="white-space:nowrap"'
    html = '<table %s>\n'%tablestyle
    for row in table:
        html += '  <tr>\n'
        for val in row:
            html += '<td %s>%s</td>\n'%(tdstyle,val)
        html += '  </tr>\n'
    html += '</table>'
    return html

def xlsx2html(xlsxfile,title = ['all']):
    t = Tables()
    t.load_xlsx(xlsxfile)
    output = ''
    if title[0] == 'all':
        for title in t.titles:
            output += ('%s\n'%title).encode('utf-8')
            output += table2html(t.tables[title]).encode("utf-8")
            output += '<br/>\n'.encode('utf-8')
    else:
        for n in num:
            output += tables[int(n)].encode("utf-8")
            output +=  '<br/>\n'.encode('utf-8')
    return output

class Tables():
    def __init__(self):
        self.titles = []
        self.tables = {}
    def load_xlsx(self,xlsx_file):
        wb = load_workbook(filename = xlsx_file)
        sheet_ranges = wb.get_active_sheet()

        table = 0
        row = 0
        row_empty = 0
        row_max_empty = 100
        end = False
        th = None
        while not end:
            col = []
            col_empty = 0
            col_max_empty = 3
            col_end = False
            while not col_end:
                value = sheet_ranges.cell(row=row,column=len(col)).value
                if value:
                    col_empty = 0
                else:
                    value = ''
                    col_empty += 1
                col.append(value)
                if col_empty >= col_max_empty:
                    col = col[:-col_max_empty]
                    col_end = True
            row += 1
            if len(col) == 1:
                if not th:
                    th = col[0]
                    worktable = []
                else:
                    if th == "" and worktable == []:
                        pass
                    else:
                        self.titles.append(th)
                        self.tables[th] = worktable
                    th = col[0]
                    worktable = []
            elif len(col) > 1:
                if not th:
                    th = ""
                    worktable = []
                worktable.append(col)
                row_empty = 0
            else:
                row_empty += 1
            if row_empty >= row_max_empty:
                end = True
                self.titles.append(th)
                self.tables[th] = worktable

if __name__ == "__main__":
    print xlsx2html(sys.argv[1],sys.argv[2:])

