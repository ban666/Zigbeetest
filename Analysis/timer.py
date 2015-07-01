#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
__author__ = 'liaoben'

import os,time,sys
from DataAnalysis import *

def sendReport():
    rtime,fname = gen_Report()
    txt=excelp.excelReadForMail(fname)
    #print txt
    zipout = gen_Zipfile()
    ptext = r'''测试时间：
    '''+rtime[0]+'-'+rtime[1]+r'''

    测试设备：100个节点

    本轮测试结果：
    '''+txt+r'''
    数据详见附件
    '''
    gen_Email(ptext,attfile=zipout)

def senEmailByTime(sendtime):
    while 1:
        date = time.strftime("%H%M", time.localtime())
        if date==sendtime:
            sendReport()
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'宜家龙臣测试报告发送成功'
            time.sleep(61)

if __name__ == '__main__':
    sendtime=conf_Loading()[2]
    senEmailByTime(sendtime)