#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
# @Date:   2015-03-26 11:16:31
# @Last Modified by:   anchen
# @Last Modified time: 2015-05-29 09:49:52
import xlsxwriter,xlrd
'''
workbook = xlsxwriter.Workbook('excel.xlsx')
ws = workbook.add_worksheet()


data = xlrd.open_workbook('excel.xlsx')
table = data.sheets()[0]  

nrows = table.nrows
 
ncols = table.ncols

print nrows,ncols
for i in range(nrows):
    print table.row_values(i)

for i in range(10):
    ws.write(i,0,i+1)

workbook.close()
'''

def ExcelWriteForAna(fname,data):
    wb = xlsxwriter.Workbook(fname)
    ws = wb.add_worksheet()
    columnlist=[u'设备ID',u'设备mac',u'设备种类',u'组网信息数据条数',u'状态信息数据条数',u'异常数据条数',u'掉线数据次数',u'掉网次数',u'应答数据条数',u'应答数据_去重',u'数据开始时间',u'数据结束时间']
     
    ws.set_column(0,11,22)
    #column
    for i in range(12):
        ws.write(0,i,columnlist[i])
    
    for i in range(len(data)):
        for j in range(12):
            #print data[i][j]
            ws.write(i+1,j,str(data[i][j]).decode('utf-8'))

    wb.close()

