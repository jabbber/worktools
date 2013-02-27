#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
from openpyxl.reader.excel import load_workbook
from openpyxl import Workbook
from openpyxl.cell import get_column_letter

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
    def __table2html(self,table):
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
    def gethtml(self,titles = ['all']):
        output = ''
        if titles[0] == 'all':
            for title in self.titles:
                output += ('%s\n'%title).encode('utf-8')
                output += self.__table2html(self.tables[title]).encode("utf-8")
                output += '<br/>\n'.encode('utf-8')
        else:
            for title in titles:
                title = title.decode('utf-8')
                output += ('%s\n'%title).encode('utf-8')
                output += self.__table2html(self.tables[title]).encode("utf-8")
                output += '<br/>\n'.encode('utf-8')
        return output
    def getxlsx(self,dest_filename):
        wb = Workbook()
        ws = wb.worksheets[0]
        row_num = 0
        for title in self.titles:
#            ws.append([title])
            row_num += 1
            ws.cell('%s%s'%(get_column_letter(1), row_num)).value = title
            row_num += 1
            for row in self.tables[title]:
#                ws.append(row)
                row_num += 1
                col_num = 0
                for col in row:
                    col_num += 1
                    ws.cell('%s%s'%(get_column_letter(col_num), row_num)).value = col
            row_num += 1
        wb.save(filename = dest_filename)

def xlsx2html(xlsxfile,titles = ['all']):
    t = Tables()
    t.load_xlsx(xlsxfile)
#    t.getxlsx("test.xlsx")
    return t.gethtml(titles)

if __name__ == "__main__":
    print xlsx2html(sys.argv[1],sys.argv[2:])

