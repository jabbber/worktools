#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
from openpyxl.reader.excel import load_workbook
from openpyxl import Workbook
from openpyxl.cell import get_column_letter
import openpyxl.style

class Tables():
    def __init__(self):
        self.titles = []
        self.tables = {}
    def load_xlsx(self,xlsx_file):
        wb = load_workbook(filename = xlsx_file)
        sheet_ranges = wb.get_active_sheet()
#        print sheet_ranges.get_style('A7')

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
            row += 1
        return 0
    def __table2html(self,table):
        WIDTH = {'序号':20,
                }
        tablestyle = "width=1300 style='BORDER-BOTTOM-STYLE: solid; BORDER-RIGHT-STYLE: solid; BORDER-TOP-STYLE: solid; BORDER-LEFT-STYLE: solid' border=1 cellSpacing=0 borderColor=#000000 cellPadding=1 bgColor=#ffffff"
        tdstyle = 'style="white-space:nowrap"'
        html = '<table %s>\n'%tablestyle
        for row in table:
            if row[0] == '序号'.decode('utf-8'):
                html += '  <tr>\n'
                for val in row:
                    if WIDTH.has_key(val.encode('utf-8')):
                        width = WIDTH[val.encode('utf-8')]
                        html += u"<td width=%s ><NOBR><FONT size=2 face=宋体 color=#0909f7><STRONG>%s</STRONG></FONT></NOBR></td>"%(width,val)
                    else:
                        html += u"<td width=120 ><NOBR><FONT size=2 face=宋体 color=#0909f7><STRONG>%s</STRONG></FONT></NOBR></td>"%val
                html += '  </tr>\n'
            else:
                html += '  <tr>\n'
                for val in row:
                    html += u"<td style='word-break:break-all' ><FONT size=2 face=宋体  >%s</FONT></td>"%val
                html += '  </tr>\n'
        html += '</table>'
        return html
    def __xlsx_setstyle(self,style,style_string):
        argv = style_string.split(':')
        n = 0
        fields = {'font':('name','size','bold','italic','superscript','subscript','underline','strikethrough','color'),
                'fill':('fill_type','rotation','start_color','end_color'),
                'borders':('left','right','top','bottom','diagonal','diagonal_direction','all_borders','outline','inside','vertical','horizontal'),
                'alignment':('horizontal','vertical','text_rotation','wrap_text','shrink_to_fit','indent'),
                'number_format':('_format_code','_format_index'),
                'protection':('locked','hidden')
                }
        for obj in ('font','fill','borders','alignment','number_format','protection'):
            for val in fields[obj]:
                if obj == 'borders' and val != 'diagonal_direction':
                    for val_1 in ('border_style','color'):
                        exec "style.%s.%s.%s = eval(argv[n])"%(obj,val,val_1)
                        n += 1
                else:
                    exec "style.%s.%s = eval(argv[n])"%(obj,val)
                    n += 1
        return style
    def gethtml(self,titles = ['all']):
        output = ''
        if titles[0] == 'all':
            for title in self.titles:
                output += ('%s\n'%title)
                output += self.__table2html(self.tables[title])
                output += '<br/>\n'
        else:
            for title in titles:
                title = title.decode('utf-8')
                output += ('%s\n'%title)
                output += self.__table2html(self.tables[title])
                output += '<br/>\n'
        return output.encode('utf-8')
    def getxlsx(self,dest_filename):
        wb = Workbook()
        ws = wb.worksheets[0]
        row_num = 0
        for title in self.titles:
#            ws.append([title])
            row_num += 1
            cell = ws.cell('%s%s'%(get_column_letter(1), row_num))
            cell.value = title
            row_num += 1
            for row in self.tables[title]:
#                ws.append(row)
                row_num += 1
                col_num = 0
                for col in row:
                    col_num += 1
                    cell = ws.cell('%s%s'%(get_column_letter(col_num), row_num))
                    cell.value = col
            row_num += 1
        wb.save(filename = dest_filename)

def xlsx2html(xlsxfile,titles = ['all']):
    t = Tables()
    t.load_xlsx(xlsxfile)
#    t.getxlsx("test.xlsx")
    return t.gethtml(titles)

if __name__ == "__main__":
    print xlsx2html(sys.argv[1],sys.argv[2:])

