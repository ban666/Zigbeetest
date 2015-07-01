# -*- coding:utf-8 -*-

__author__ = 'Liao Ben'

'''
    Library for Analyzing Zigbee_data
'''
import os,re,time,excelp

class ConfigAnalysis:
    '''
    Library for Analyzing Zigbee_data
    '''
    def __init__(self,file,outputFolder):
        self.file=file
        self.outputFolder=outputFolder
        self.list1=[]
        self.list2=[]
        self.list3=[]
        self.devicedict={
        '01':'智能路由节点',
        '04':'智能调光器',
        '03':'智能门磁感应器',
        '06':'智能全向红外网关',
        '0d':'智能烟雾感应器',
        '0f':'一氧化碳感应器',
        '0c':'人体红外感应器',
        '0e':'可燃气体感应器',
        '14':'智能单开',
        '15':'智能双开',
        '16':'智能三开',
        '11':'智能报警器',
        '13':'红外水晶开关',
        '17':'智能窗帘',
        '18':'智能窗户'
        }
        self.length=set()
        self.iddict={}
        
        self.errdict={
        "04":[48,36,42,'f10200'],
        "03":[52,36,42,'f10400'],
        '0c':[52,36,42,'f10400'],
        '0d':[52,36,42,'f10400'],
        '0e':[76,42,44,'00'],
        '13':[52,36,42,'f10400'],
        '14':[46,36,44,'f1010001'],
        '15':[48,36,44,'f1020000'],
        '16':[50,36,46,'f103000000'],
        '17':[50,36,46,'f103000000']
        }

        self.replylist=['04','11','14','15','16','17','18','06']


    def FileCheck_Comread(self):
        '''
        get data from file
        '''
        with open(self.file,'r') as f:
            for i in f:
                self.list1.append(i.rstrip())
                self.list2.append(i[20::].rstrip())
                self.list3.append(i[0:19])
                self.length.add(len(i[20::].rstrip()))
        if not os.path.exists(self.outputFolder):
            try:
                os.makedirs(self.outputFolder)
            except Exception as e:
                pass


    def FileCheck_debug(self):
        '''
        get data from file(format as debug_hhy)
        '''
        with open(self.file,'r') as f:
            pattern = re.compile('.*?:(.*)',re.S)
            year = time.strftime("%Y", time.localtime())
            for i in f:
                item=re.findall(pattern,i)
                if len(item)==1:
                    tempstr=''.join([year,'-',item[0]])[0:19]
                    self.list3.append(tempstr)
                elif len(i.strip())!=0:
                    self.list2.append(i.strip())
            for i in range(len(self.list2)):
                tlist=[self.list3[i],self.list2[i]]

                self.list1.append(" ".join(tlist))
        if not os.path.exists(self.outputFolder):
            try:
                os.makedirs(self.outputFolder)
            except Exception as e:
                pass


    def Filecheck1(self,stra):
        '''
        check whether the data is valid and stitching
        :param stra: string object like 'f8','f8e6'
        '''
        for i in range(len(self.list2)+2):
            try:
                if self.list2[i].find(stra)!=0:
                    self.list2[i-1]=str(self.list2[i-1])+str(self.list2[i])
                    self.list2.pop(i)
                    self.list1[i-1]=self.list3[i-1]+" "+self.list2[i-1]
                    self.list1.pop(i)
                    self.list3.pop(i)
            except Exception as e:
                pass

    def Filecheck2(self):
        '''
        check whether the data is valid and stitching
        '''
        for i in range(len(self.list2)+2):
            try:
                if self.list2[i].count('f8e6')>=2:
                    tempstr=self.list2[i].split('f8e6')
                    tempstr.pop(0)
                    for str in tempstr:
                        str1='f8e6'+str
                        self.list2.insert(i+1,str1)
                        self.list3.insert(i+1,self.list3[i])
                        self.list1.insert(i+1,self.list3[i]+" "+str1)
                    self.list1.pop(i)
                    self.list2.pop(i)
                    self.list3.pop(i)
            except Exception as e:
                pass    

    def GetStatus(self):
        '''
        check whether the data is completely legal
        :return: 0:the date is completely legal
                 1:the date isn't completely legal
        '''
        for i in self.list2:
            if i.find('f8')!=0:
                return 1
            if i.find('f8e6')!=0:
                return 1
            if i.count('f8e6')>=2:
                return 1
        return 0


    def FileConnect_Comread(self):
        '''
        splicing data until the data was completely legal
        '''
        self.FileCheck_Comread()
        status=self.GetStatus()
        while 0!=status:
            self.Filecheck1('f8')
            self.Filecheck1('f8e6')
            self.Filecheck2()
            status=self.GetStatus()
        
        result=[self.list1,self.list2,self.list3]
        date = self.list3[0][0:10].replace('-','')
        wfile=self.outputFolder+date+".txt"
        tlist=[]
        id_typelist=[]
        with open(wfile,'w') as f:
            for i in self.list1:
                if len(i)>=48 and self.devicedict.has_key(i[34:36]):
                    tlist.append(i[34:36])
                if i[24:28]!='0000' and len(i)>=48 and self.devicedict.has_key(i[34:36]):
                    tlistb=i[24:28]+i[34:36]
                    id_typelist.append(tlistb)
                f.write(i)
                f.write('\n')
                f.flush()
        #print set(tlist)
        for i in list(set(id_typelist)):
            if len(i)==6:
                self.iddict[i[0:4]]=i[4:6]
        #print self.iddict
        for i in set(tlist):
            try:
                path=self.outputFolder+self.devicedict[i].decode('utf-8')
                os.makedirs(path)
            except Exception as e:
                pass
        return result


    def FileConnect_debug(self):
        '''
        splicing data until the data was completely legal
        for file got by debug_hhy
        '''
        self.FileCheck_debug()
        for i in range(3):
            self.Filecheck1('f8')
            self.Filecheck1('f8e6')
            self.Filecheck2()
        result=[self.list1,self.list2,self.list3]
        date = self.list3[0][0:10].replace('-','')
        wfile=self.outputFolder+date+".txt"
        tlist=[]
        id_typelist=[]
        with open(wfile,'w') as f:
            for i in self.list1:
                tlist.append(i[34:36])
                if i[24:28]!='0000':
                    tlistb=i[24:28]+i[34:36]
                    id_typelist.append(tlistb)
                f.write(i)
                f.write('\n')
                f.flush()
        for i in list(set(id_typelist)):
            self.iddict[i[0:4]]=i[4:6]
        #print self.iddict
        for i in set(tlist):
            try:
                path=self.outputFolder+self.devicedict[i].decode('utf-8')
                os.makedirs(path)
            except Exception as e:
                pass
        return result

    #根据对应id分类数据
    #type为文件种类：1、debug_hhy所得数据，2、Comread所得数据
    def GetDate(self,type=1):
        '''
        splicing data for different file type
        :param type:different file type 1.debug_hhy 2.comread
        :return:
        '''
        if type==1:
            result=self.FileConnect_debug()
        elif type==2:
            result=self.FileConnect_Comread()
        else:
            print 'Error!'
        date = self.list3[0][0:10].replace('-','')
        for i,k in self.iddict.items():
            idlist=[]
            dtype = self.devicedict[k].decode('utf-8')
            wfile=self.outputFolder+dtype+'/'+date+'_'+i+'.txt'   
            for j in result[0]:
                if j[24:28]==i:
                    idlist.append(j.strip())
            with open(wfile,'w') as f:
                for l in idlist:
                    f.write(l.strip())
                    f.write('\n')
                    f.flush()
        result=[self.list1,self.list2,self.list3,self.iddict]
        return result

    #根据ID获取对应节点异常数据条数，并保存到文件
    def GetErrById(self,id,length,sid,did,stra):
        '''
        get error messages count,and save the error massage to file
        :param id:string object that like '0004',device id
        :param length:int object that like 52,message length
        :param sid:int object that like 30,message length
        :param did:int object that like 52,message length
        :param stra:string object that like 'f1040000',the correct string
        :return:
        '''
        date = self.list3[0][0:10].replace('-','')
        idlist = []
        lista = []
        listb = []
        type = self.devicedict[self.iddict[id]].decode('utf-8')  
        for j in self.list1:
            if j[24:28]==id:
                lista.append(j)
            if j[24:28]==id and len(str(j))==length and j[sid:did]!=stra:
                listb.append(j)
        print "mac为 ",id,"的",type,"设备共有",len(lista),'条数据'
        print "mac为 ",id,"的","误报数据共有",len(listb),'条'
        wfile=self.outputFolder+type+'/'+date+'_'+id+'_error.txt'
        with open(wfile,'w') as f:
            for l in listb:
                f.write(l.strip())
                f.write('\n')
                f.flush()

    def GetTimeStoE(self):
        '''
        get the start time and the end time
        :return:list object that like['2015-05-15 17:20:31','2015-05-16 17:20:31']
        '''
        result = [self.list1[0][:20],self.list1[-1][:20]]
        return result

    #根据不同设备类型获取信息，分边保存到对应文件,仅支持带有状态位的设备
    def GetErrByType(self,ttype,time_range=600):
        '''
        get all infomation and save to file by different device type.
        :param ttype: sting object that like '04','11'. device type
        :param time_range: int object that like 300,100. timeout
        :return: infomation list
        '''
        date = self.list3[0][0:10].replace('-','')
        idlist = []
        type = self.devicedict[ttype].decode('utf-8')  
        tlen = self.errdict[ttype][0]
        sid  = self.errdict[ttype][1]
        did  = self.errdict[ttype][2]
        tstr = self.errdict[ttype][3] 
        result = []

        for i,j in self.iddict.items():
            if j==ttype:
                idlist.append(i)
        for i in idlist:
            mac=''
            timelist=[]
            losecount=0
            timeout_list=[]
            lista = []
            listb = []
            listc = []
            listd = []
            list3=[]
            list4=[]
            gdata_length=0
            idata_length=0
            for j in self.list1:
                if j[24:28]==i:
                    lista.append(j)
                    timelist.append(j[0:19])
                if j[24:28]==i and len(str(j))==tlen and j[sid:did]!=tstr:
                    listb.append(j)
                if j[24:28]==i and j[36:38]=='f4':
                    listd.append(j)
            for k in lista:
                if len(k)==72:
                    mac=k[40:56]
                    gdata_length+=1
                else:
                    idata_length+=1
            for m in self.list1:
                if len(m)==62 and m[36:56]=='a209'+mac:
                    #print m
                    if m[0:19]>timelist[0]:
                        #print m,timelist[0]
                        losecount+=1
                        listc.append(m)
            for l in range(len(timelist)-1):
                TimeR=self.TimeRange(timelist[l],timelist[l+1])
                list4.append(TimeR)
                if int(TimeR)>time_range:
                    #print TimeR
                    #print list1[l]
                    #print list1[l+1]
                    tout_list=[lista[l],lista[l+1],TimeR]
                    timeout_list.append(tout_list)
                    list3.append(timelist[l])
            listd_without_repeat=len(set(listd))            
            averagetime=self.GetAverage(list4)
            rlist=[i,mac,type.encode('utf-8'),gdata_length,idata_length,len(listb),len(list3),losecount,len(listd),listd_without_repeat,lista[0][0:20],lista[-1][0:20]]
            result.append(rlist)
            wfile=self.outputFolder+type+'/'+date+'_'+i+'_error.txt'
            wfile2=self.outputFolder+type+'/'+date+'_'+i+'_Loseconnect.txt'
            wfile3=self.outputFolder+type+'/'+date+'_'+i+'_reply.txt'
            wfile4=self.outputFolder+type+'/'+date+'_'+i+'_timeout.txt'
            with open(wfile,'w') as f:
                for l in listb:
                    f.write(l.strip())
                    f.write('\n')
            with open(wfile2,'w') as f:
                for l in listc:
                    f.write(l.strip())
                    f.write('\n')
            with open(wfile3,'w') as f:
                for l in listd:
                    f.write(l.strip())
                    f.write('\n')
            with open(wfile4,'w') as f:
                for l in timeout_list:
                    f.write(str(l).strip())
                    f.write('\n')
        return result

    #根据不同设备类型获取信息，分边保存到对应文件,仅支持不带状态位的设备
    def GetInFoByType(self,ttype,time_range=600):
        '''
        get all infomation and save to file by different type.
        :param ttype: sting object that like '04','11'. device type
        :param time_range: int object that like 300,100. timeout
        :return:infomation list
        '''
        date = self.list3[0][0:10].replace('-','')
        idlist = []
        type = self.devicedict[ttype].decode('utf-8')  
        result = []
        
        for i,j in self.iddict.items():
            if j==ttype:
                idlist.append(i)
        for i in idlist:
            mac=''
            timelist=[]
            list3=[]
            list4=[]
            gdata_length=0
            idata_length=0
            losecount=0
            timeout_list=[]
            lista = []
            listb = []
            listc = []
            listd = []
            for j in self.list1:
                if j[24:28]==i:
                    lista.append(j)
                    timelist.append(j[0:19])
                if j[24:28]==i and j[36:38]=='f4':
                    listd.append(j)
            for k in lista:
                if len(k)==72:
                    mac=k[40:56]
                    gdata_length+=1
                else:
                    idata_length+=1
            for m in self.list1:
                if len(m)==62 and m[36:56]=='a209'+mac:
                    #print m
                    if m[0:19]>timelist[0]:
                        #print m,timelist[0]
                        losecount+=1
                        listc.append(m)
            for l in range(len(timelist)-1):
                TimeR=self.TimeRange(timelist[l],timelist[l+1])
                list4.append(TimeR)
                if int(TimeR)>time_range:
                    #print TimeR
                    tout_list=[lista[l],lista[l+1],TimeR]
                    timeout_list.append(tout_list)
                    list3.append(timelist[l])
            averagetime=self.GetAverage(list4)  
            listd_without_repeat=len(set(listd))
            rlist=[i,mac,type.encode('utf-8'),gdata_length,idata_length,0,len(list3),losecount,len(listd),listd_without_repeat,lista[0][0:20],lista[-1][0:20]]
            result.append(rlist)
            wfile=self.outputFolder+type+'/'+date+'_'+i+'_Loseconnect.txt'
            wfile2=self.outputFolder+type+'/'+date+'_'+i+'_reply.txt'
            wfile3=self.outputFolder+type+'/'+date+'_'+i+'_timeout.txt'
            with open(wfile,'w') as f:
                for l in listc:
                    f.write(l.strip())
                    f.write('\n')
            with open(wfile2,'w') as f:
                for l in listd:
                    f.write(l.strip())
                    f.write('\n')
            with open(wfile3,'w') as f:
                for l in timeout_list:
                    f.write(str(l).strip())
                    f.write('\n')
        return result

    def GetRepeatId(self):
        '''
        check whether the content has repeated id.
        :return:list objecet that like['04','0c'].device type who were given a duplicated ID
        '''
        idlist=[]
        for i,j in self.iddict.items():
            idlist.append(i)
        for i in idlist:
            typelist = []
            lista = []
            for j in self.list1:
                if j[24:28]==i:
                    lista.append(j)
            for k in lista:
                typelist.append(k[34:36])
            typelist=list(set(typelist))
            if len(typelist)>1:
                print i,typelist
        return typelist


    def TimeRange(self,a,b):
        '''
        computing time
        :param a:string object.start time
        :param b:string object.end time
        :return:int object.time difference
        '''
        time1=time.mktime(time.strptime(a,'%Y-%m-%d %H:%M:%S'))
        time2=time.mktime(time.strptime(b,'%Y-%m-%d %H:%M:%S'))
        return time2-time1

    def GetAverage(self,lista):
        r=0
        for i in lista:
            r+=i
        if len(lista)==0:
            return 0
        return r/len(lista)


    def GetAllErrByType(self,time_range=600):
        '''
        get all information and save to file.
        :param time_range: int object.time range
        :return:list object contains all infomation to write to excel
        '''
        list1=[]
        result=[]
        for i,j in self.iddict.items():
            list1.append(j)
        for i in list(set(list1)):
            type = self.devicedict[i].decode('utf-8')  
            print "=====================",type,"====================="
            if self.errdict.has_key(i):
                rlist=self.GetErrByType(i,time_range)
                print len(rlist)
            else:
                rlist=self.GetInFoByType(i,time_range)
                print len(rlist)
            for j in rlist:
                result.append(j)
        print len(result)
        return result

    def WriteToExcel(self,data):
        '''
        save the infomation to excel.
        :param data: list object got by GetAllErrByType()
        :return:string object.file name
        '''
        date = self.list3[0][:19].replace(' ','').replace('-','').replace(':','')
        fname=self.outputFolder+date+'_'+'_Excel.xlsx'
        excelp.ExcelWriteForAna(fname,data)
        return fname

