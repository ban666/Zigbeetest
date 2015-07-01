# -*- coding:utf-8 -*-
 
import os,sys,ConfigParser
from Lib.Ana2 import *
from Lib import ssh,zip,maillib,excelp
from Config import mailinfo as m

ofolder=''
def conf_Loading(confgfile='work.cfg'):
    global ofolder
    config=ConfigParser.ConfigParser()
    with open(confgfile,"r") as cfgfile:
        config.readfp(cfgfile)
        op=config.options("conf")
        work_directory = config.get('conf','work_directory')
        server = config.get('conf','server')
        port = int(config.get('conf','port'))
        username = config.get('conf','username')
        password = config.get('conf','password')
        rfile = config.get('conf','rfile')
        get_way=config.get('conf','getway')
        forAnafile = config.get('conf','foranafile')
        sendtime = config.get('conf','sendtime')
    date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    ofolder=work_directory+date+'/'
    if not os.path.isdir(ofolder):
        os.makedirs(ofolder)
    if get_way=='yjlc':
        readfile=ssh.getScp(server,port,username,password,rfile)
    else:
        readfile=forAnafile

    result = [ofolder,readfile,sendtime]
    return result

def get_Content(confgfile='work.cfg'):
    conf_content=conf_Loading(confgfile)
    ofolder=conf_content[0]
    readfile=conf_content[1]
    #print readfile
    cfg=ConfigAnalysis(readfile,ofolder)
    return cfg

def gen_Report(time_range=900,confgfile='work.cfg'):
    cfg = get_Content()
    result = cfg.GetDate(2)
    e=cfg.GetAllErrByType(time_range=900)
    excelf=cfg.WriteToExcel(e)
    time=cfg.GetTimeStoE()
    return time,excelf

def gen_Zipfile():
    global ofolder
    date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    zipout = os.getcwd()+'/Zipfile/'+date+'.zip'
    zip.zip_dir(ofolder,zipout)
    return zipout

def gen_Email(ptext,htext='',attfile=''):

    mailresult=maillib.sendEmail(m.server,m.user,m.password, m.fromAdd, m.toAdd, m.subject, ptext, htext,attfile)
    if not mailresult:
        print mailresult

if __name__ == '__main__':
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
