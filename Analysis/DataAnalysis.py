# -*- coding:utf-8 -*-
 
import os,sys,ConfigParser
from Lib.Ana2 import *
from Lib import ssh,zip,maillib
from Config import mailinfo as m

# server='192.168.2.100'
# port=8700
# username='root'
# password='zhangmin123'
# rfile='zigbeelog'
# readfile=ssh.getScp(server,port,username,password,rfile)
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
    date = time.strftime("%Y%m%d%H%M%S", time.localtime())
    ofolder=work_directory+date+'/'
    readfile=ssh.getScp(server,port,username,password,rfile)
    result = [ofolder,readfile]
    return result

def get_Content(confgfile='work.cfg'):
    conf_content=conf_Loading(confgfile)
    ofolder=conf_content[0]
    readfile=conf_content[1]
    cfg=ConfigAnalysis(readfile,ofolder)
    return cfg

def gen_Report(time_range=600,confgfile='work.cfg'):
    cfg = get_Content()
    result = cfg.GetDate(2)
    e=cfg.GetAllErrByType(time_range=600)
    cfg.WriteToExcel(e)
    time=cfg.GetTimeStoE()
    return time

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
    rtime = gen_Report()
    zipout = gen_Zipfile()
    ptext = r''' 测试时间：
    '''+rtime[0]+'-'+rtime[1]
    gen_Email(ptext,attfile=zipout)
