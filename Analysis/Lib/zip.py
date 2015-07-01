#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben

'''
    Library for zipfile
'''
import os,os.path
import zipfile

def zip_dir(dirname,zipfilename):
    '''
    compression and save the file.
    :param dirname:string object.folder name
    :param zipfilename:string object.zipfile name
    :return:
    '''
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()



