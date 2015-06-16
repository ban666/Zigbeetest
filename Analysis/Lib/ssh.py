#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
# @Date:   2015-06-06 14:51:26
# @Last Modified by:   liaoben
# @Last Modified time: 2015-06-12 14:23:41

import paramiko,os
import time
from scp import SCPClient

def SshLogin (ip,cmd,username='root',password='zhangmin123',port=8700):
   ssh = paramiko.SSHClient()
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   ssh.connect(ip,port,username,password)
   for i in cmd:
    print i
    stdin,stdout,stderr = ssh.exec_command(i)
    print 1111
    #print stdout.readlines()

def SshLogin2 (ip,cmd,username='root',password='zhangmin123',port=8700):
   ssh = paramiko.SSHClient()
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   ssh.connect(ip,port,username,password)
   stdin,stdout,stderr = ssh.exec_command(cmd)
   '''
   b = stdout.readlines()
   c = stderr.readlines()
   print a,b,c
   return a
   '''
def getScp(server,port,username,password,rfile):
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect(server,port,username,password)
  #date = time.strftime("%Y%m%d%H%M%S", time.localtime())
  lfile = rfile+'.txt'
  print lfile
  with SCPClient(ssh.get_transport()) as scp:
    scp.get(rfile,lfile)
  return lfile
username='root'
password = 'zhangmin123'
server='192.168.2.105'
port=8700
rfile = 'zigbeelog'
#getScp(server,port,username,password,rfile)
# sftp = ssh.open_sftp()
# remote_file = sftp.file(remotepath,"wb")
# remote_file.set_pipelined(True)
# remote_file.write(data)
# sftp.close()
# ssh.close()