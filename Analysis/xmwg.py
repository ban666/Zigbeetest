#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
# @Date:   2015-03-30 10:14:29
# @Last Modified by:   anchen
# @Last Modified time: 2015-06-02 15:30:19
import os,sys,time,socket,test

def cmd_g(dat):
    l='{:008x}'.format(len(dat))
    tlist1='000000000000'+l+'0000'
    return tlist1

def cmd_send(sid,dat):
    tlist=cmd_g(dat)
    tstr=tlist.decode('hex')+dat
    recvd=''
    buffer=100
    #print tstr
    try:
        sid.send(tstr)
        while True:
            recvdata=s.recv(buffer)
            recvd+=recvdata
            if not len(recvdata)==buffer:
                break
        result=recvd.encode('hex')[24:].decode('hex')    
    except Exception as e:
        print e
        return e
    return result

def check_online(sid,mac):
    tstr='State@'
    for i in mac:
        tstr=tstr+i+','
    tstr=tstr.rstrip(',')
    result=cmd_send(sid,tstr)
    #print result
    rlist=result.split('00124b')[1:]
    tlist=[]
    for i in rlist:
        tstr2='00124b'+i[0:11]+i[-1]
        tlist.append(tstr2)
    
    return tlist

def device_access(sid,mac_type):
    tstr='MacIn@'
    for i in mac_type:
        tstr=tstr+i+','
    tstr=tstr.rstrip(',')
    print tstr
    result=cmd_send(sid,tstr)
    return result

def device_logout(sid,mac):
    tstr='MacOut@'
    for i in mac:
        tstr=tstr+i+','
    tstr=tstr.rstrip(',')
    result=cmd_send(sid,tstr)
    return result

def device_control(sid,mac_status):
    
    for i in mac_status:
        tstr='Ctrl@'
        tstr=tstr+i
        tlist=cmd_g(tstr)
        tstr1=tlist.decode('hex')+tstr
        #print tstr1
        sid.send(tstr1)
        time.sleep(3)

def get_mac_type(list1,list2):
    tlist=[]
    for i in list1:
        if i[-1]!='1':
            tlist.append(i[:16])
    tlist2=[x[:16] for x in list2]
    tlist3=[]
    for i in tlist:
        tlist3.append(list2[tlist2.index(i)])
    print len(tlist3)
    print tlist3
    return tlist3

def cmd_generate(mac_type,type_cmd_dict):
    cmdlist=[]
    for i in mac_type:
        if type_cmd_dict.has_key(i[-2:]):
            tcmd=type_cmd_dict[i[-2:]]
            for j in tcmd:
                tstr=i[:16]+':'+j
                cmdlist.append(tstr)
    return cmdlist            

type_cmd_dict={
'04':['1#15','2'],
#'11':['1','2'],
'14':['1','2'],
'15':['3','4'],
'16':['3','4'],
'17':['1','3'],
'18':['1','3'],
'06':['1','2']
}

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ad=('192.168.2.103',8988)
s.connect(ad)

mac=['00124b0003a1cc59','00124b0004f074e8']
mac_status=['00124b000520c404:4','00124b000520c718:4']
mac_drop_list=['00124b0004f0076f','00124b0004f0077c','00124b0004eff2fb','00124b0004efcf9d','00124b0004f00764','00124b0004f0077c','00124b0004efcf9d']
mac_access_list=['00124b000520cb3c0e', '00124b000520c83a0e', '00124b000520cc7b0e', '00124b000520c8720e', '00124b000520cb620e', '00124b0004f0072317', '00124b0004efc02917', '00124b0004f004f617', '00124b0004f004f417', '00124b0004f0071c17']

mac_type=test.mac_type_list

#print device_logout(s,mac_drop_list)
device_access(s,test.mac_type_list)
print len(test.mac_type_list)
#device_logout(s,['10001'])
#device_control(s,mac_status)
#print len(test.mac_list)

s.close()
