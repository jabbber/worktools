#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os,sys
import traceback
import re
from bs4 import BeautifulSoup
from openpyxl.reader.excel import load_workbook
from openpyxl import Workbook
from openpyxl.cell import get_column_letter
from openpyxl.styles import colors, Style, PatternFill, Border, Side, Alignment, Protection, Font

class Tables():
    def __init__(self):
        self.titles = []
        self.tables = []
        self.hostlist = None
        self.blacklist = None
    def clear(self):
        """clear the data have been loaded.
        """
        self.titles = []
        self.tables = []
    def load(self,filename):
        """load data from given file path,the file can be .xlsx or .htm(l)
        """
        name, ext = os.path.splitext(filename)
        if ext == ".xlsx":
            try:
                self.load_xlsx(filename)
            except:
                print traceback.print_exc()
                return False
        elif ext in ('.htm','.html'):
            try:
                self.load_html(filename)
            except:
                print traceback.print_exc()
                return False
        else:
            print "error: can load %s!"%filename
            return False
        return True
    def load_html(self,html_file):
        html = file(os.path.realpath(html_file),'r').read().decode('utf-8')
        soup = BeautifulSoup(html)
        if soup.html:
            tables = soup.html.body.find_all('table',recursive=False)
        else:
            tables = soup.find_all('table',recursive=False)
        for table in tables:
            try:
                title = table.find_previous('p').get_text().encode('utf-8')
            except:
                title = ''
            self.titles.append(title)
            self.tables.append([])
            for row in table.find_all('tr',recursive=False):
                line = []
                for val in row.find_all('td',recursive=False):
                    value = val.get_text().strip()
                    if type(value) == unicode:
                        value = value.encode('utf-8')
                    line.append(value)
                if self.__black_filter(line):
                    pass
                elif self.__host_filter(line):
                    self.tables[-1].append(line)
                else:
                    pass
    def load_xlsx(self,xlsx_file):
        wb = load_workbook(filename = xlsx_file)
        sheet_ranges = wb.active
        row = 1
        end = sheet_ranges.get_highest_row()
        th = ""
        col_max = sheet_ranges.get_highest_column()
        col_max2 = col_max
        while row <= end:
            col = []
            col_empty = 0
            col_max_empty = 5
            col_end = False
            while not col_end:
                column = len(col)+1
                value = sheet_ranges.cell(row=row,column=column).value
                if value:
                    if type(value) == unicode:
                        value = value.encode('utf-8').strip()
                    col_empty = 0
                else:
                    value = ''
                    col_empty += 1
                col.append(value)
                if column >= col_max2:
                    col_end = True
                elif col_empty >= col_max_empty:
                    col = col[:-col_empty]
                    col_end = True
            if len(col) == 1:
                if th:
                    self.titles.append(th)
                    self.tables.append(worktable)
                    col_max2 = col_max
                th = col[0]
                worktable = []
            elif len(col) > 1:
                if self.__black_filter(col):
                    pass
                elif th and self.__host_filter(col):
                    worktable.append(col)
                    if col[0] == '序号':
                        col_max2= len(col)
            row += 1
        self.titles.append(th)
        self.tables.append(worktable)
        return 0
    def __load_xlsx_list(self,xlsx_file):
        wb = load_workbook(filename = xlsx_file)
        sheet_ranges = wb.active
        end = sheet_ranges.get_highest_row()
        row = 1
        keyset = set()
        while row <= end:
            value = sheet_ranges.cell(row=row,column=1).value
            if type(value) == unicode:
                keyset.add(value.encode('utf-8'))
            row += 1
        return keyset
    def load_list(self,list_file):
        """load a list from a text or xlsx file,return python set type.
        """
        if not list_file:
            keyset = set()
        elif list_file[-5:] == '.xlsx':
            keyset = self.__load_xlsx_list(list_file)
        else:
            with open(list_file) as list_f:
                keyset = set()
                for line in list_f:
                    if line.strip():
                        keyset.add(line.strip())
        return keyset
    def __filter(self,row,keyset):
        for value in row:
            if type(value) == str:
                if value in keyset:
                    return True
        return False
    def __host_filter(self,row):
        keyset = self.hostlist
        if not keyset:
            return True
        if '序号' == row[0]:
            return True
        else:
            return self.__filter(row,keyset)
    def __black_filter(self,row):
        keyset = self.blacklist
        if not keyset:
            return False
        else:
            return self.__filter(row,keyset)
    def get_html(self,titles = 'all'):
        """return the tables you given titles use html table format,default is all tables.
        """
        tables = self.tables
        output = ''
        if titles == 'all':
            for i, title in enumerate(self.titles):
                output += ('<p>%s</p>\n'%title)
                output += table2html(tables[i])
                output += '<br/>\n'
        else:
            for title in titles.split(','):
                output += ('%s<br/>\n'%title)
                n = 0
                finded = []
                for value in self.titles:
                    if value == title:
                        finded.append(n)
                    n += 1
                for num in finded:
                    output += table2html(tables[num])
                    output += '<br/>\n'
        return output
    def get_xlsx(self,dest_filename):
        """create a .xlsx file have all data have been loaded to you given path and filename.
        """
        tables = self.tables
        wb = Workbook()
        ws = wb.worksheets[0]
        row_num = 0
        column_widths = []
        
        titlestyle = Style(font=Font(size=13))
        thstyle = Style(font=Font(size=10,bold=True,color=colors.BLUE),
                        border=Border(top=Side(border_style='medium',color=colors.BLACK),
                            bottom=Side(border_style='medium',color=colors.BLACK),
                            left=Side(border_style='medium',color=colors.BLACK),
                            right=Side(border_style='medium',color=colors.BLACK))
        )
        tdstyle = Style(font=Font(size=10),
                        border=Border(top=Side(border_style='medium',color=colors.BLACK),
                            bottom=Side(border_style='medium',color=colors.BLACK),
                            left=Side(border_style='medium',color=colors.BLACK),
                            right=Side(border_style='medium',color=colors.BLACK))
        )
        
        for title_num, title in enumerate(self.titles):
            row_num += 1
            cell = ws.cell('%s%s'%(get_column_letter(1), row_num))
            cell.value = title
            cell.style = titlestyle
            row_num += 1
            th = False
            for row in tables[title_num]:
                row_num += 1
                col_num = 0
                th = False
                for i, value in enumerate(row):
                    # count column width
                    if type(value) == str:
                        l = len(value.decode('utf-8'))
                        if l == len(value):
                            pass
                        else:
                            l = l*2
                    elif type(value) == int:
                        l = len(str(value))
                    else:
                        l = len(value)
                    if len(column_widths) > i:
                        if l > column_widths[i]:
                                column_widths[i] = l
                    else:
                        column_widths.append(l)

                    col_num += 1
                    cell = ws.cell('%s%s'%(get_column_letter(col_num), row_num))
                    cell.value = value
                    if value == '序号':
                        th = True
                if th:
                    ws.row_dimensions[row_num].style = thstyle
                else:
                    ws.row_dimensions[row_num].style = tdstyle
            row_num += 1
        for i, column_width in enumerate(column_widths):
            if column_width < 6:
                ws.column_dimensions[get_column_letter(i+1)].width = 6
            elif column_width > 40:
                ws.column_dimensions[get_column_letter(i+1)].width = 40
            else:
                ws.column_dimensions[get_column_letter(i+1)].width = column_width

        wb.save(filename = dest_filename)

TABLE_STYLE = 'border=1 cellSpacing=0 borderColor=#000000 cellPadding=1 style="font-family: 宋体, Georgia, serif;font-size:14px;word-wrap: break-word;word-break: normal"'
TH_STYLE = 'style="white-space:nowrap;font-weight:bold;color:blue"'
TD_STYLE = ''

def table2html(table):
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
            html += '  <tr>\n'
            for val in row:
                html += "<td %s>%s</td>"%(TD_STYLE,val)
            html += '  </tr>\n'
    html += '</table>'
    return html

def get_html(filename,titles = 'all',host_file = None,blacklist = None):
    t = Tables()
    if host_file:
        t.hostlist = t.load_list(host_file)
    if blacklist:
        t.blacklist = t.load_list(blacklist)
    t.load(filename)
    #t.get_xlsx('test.xlsx')
    return t.get_html(titles)

if __name__ == "__main__":
    if len(sys.argv) == 5:
        print get_html(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
    elif len(sys.argv) == 4:
        print get_html(sys.argv[1],sys.argv[2],sys.argv[3])
    elif len(sys.argv) == 3:
        print get_html(sys.argv[1],sys.argv[2])
    else:
        print """Usage:
    readxlsx.py <FILE> all/title1[,title2] [HOST_FILE] [Blacklist_FILE]

FILE can be an unix text file or xlsx file.
        """
