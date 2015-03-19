#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from openpyxl import load_workbook
wb= load_workbook('周期性的日志分析.xlsx')
sheets = {}
for sheet in wb.get_sheet_names():
    ws = wb.get_sheet_by_name(sheet)
    ws.get_cell_collection()
    table = tuple((cell.value for cell in ws.get_cell_collection()))
    if not table in sheets:
        sheets[table] = [sheet]
    else:
        sheets[table].append(sheet)

duplicate = []
for sheet in sheets.values():
    if len(sheet) > 1:
        duplicate.extend(sheet)

duplicate.sort()
for sheet in duplicate:
    print(sheet)

