#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
# @Date:   2015-03-26 11:16:31
# @Last Modified by:   liaoben
# @Last Modified time: 2015-05-29 09:49:52
import xlsxwriter,xlrd

__author__ = 'Liao Ben'

'''
    Library for dealing with excel
'''
def ExcelWriteForAna(fname,data):
    '''
    write the infomation to excel
    :param fname:string object.file name
    :param data:list object.infomation
    :return:
    '''
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

def checkLoseCount(content):
    '''
    get the lose data number.
    '''
    result=[]
    for i,j in enumerate(content):
        if j!=u'0':
            tlist=[i,j.encode('utf-8')]
            result.append(tlist)
    return result[1:]

def genTxtForLose(type_content,timeout_cotent,lose_content):
    '''
    generate text for mail
    '''
    txt=''
    timeout_result=checkLoseCount(timeout_cotent)
    txt+=r'''
    1、掉线情况：共计 %s 个设备出现掉线情况。
        ''' % str(len(timeout_result))
    for (i,j) in timeout_result:
        tmsg=r'''1个 %s 出现掉线 %s 次
        '''%(type_content[i].encode('utf-8'),j)
        txt=txt+tmsg
    lose_result=checkLoseCount(lose_content)
    txt+=r'''
    2、掉网情况：共计 %s 个设备出现入网后重新发送入网请求的现象。
        ''' % str(len(lose_result))
    for (i,j) in lose_result:
        tmsg=r'''1个 %s 发送入网请求 %s 次
        '''%(type_content[i].encode('utf-8'),j)
        txt=txt+tmsg
    return txt

def genTxtForErr_YwKr(type_content,err_content):
    '''
    generate text for mail
    '''
    txt=''
    tlist=[]
    errcount=0
    for i,j in enumerate(type_content):
        if j.encode('utf-8')=='智能烟雾感应器' or j.encode('utf-8')=='可燃气体感应器' :
            tlist.append(i)
    for i in tlist:
        if err_content[i]!=u'0':
            msg=r'''1个 %s 共有 %s 条误报
        ''' % (type_content[i].encode('utf-8'),err_content[i].encode('utf-8'))
            txt+=msg
            errcount+=1
    txt=r'''
    3、误报情况：共计 %s 个设备出现误报情况。
        ''' %str(errcount)+txt
    return txt

def excelReadForMail(fname,sheet='Sheet1'):
    '''
    get the information to send email.
    :param fname: string object.file name
    :param sheet: string object.excel sheet
    :return:string object.the mail content
    '''
    bk=xlrd.open_workbook(fname).sheet_by_name(sheet)
    txt=''
    type_content = bk.col_values(2)
    err_content = bk.col_values(5)
    timeout_cotent=bk.col_values(6)
    lose_content=bk.col_values(7)
    endtime_content=bk.col_values(11)
    txt+=genTxtForLose(type_content,timeout_cotent,lose_content)
    txt+=genTxtForErr_YwKr(type_content,err_content)
    return txt
