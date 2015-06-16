#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: liaoben
# @Date:   2015-04-15 14:38:49
# @Last Modified by:   liaoben
# @Last Modified time: 2015-06-15 11:14:05
import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib,os

def sendEmail(server,user,passwd, fromAdd, toAdd, subject, plainText, htmlText='',attFile=''):
        msg=''
        strFrom = fromAdd
        strTo = ', '.join(toAdd)

        if not (server and user and passwd) :
                print 'incomplete login info, exit now'
                return

        # 设定root信息
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        #设定纯文本信息
        msgText = MIMEText(plainText, 'plain', 'utf-8')
        msgAlternative.attach(msgText)

        #设定HTML信息
        #msgText = MIMEText(htmlText, 'html', 'utf-8')
        #msgAlternative.attach(msgText)

        #添加附件
        if attFile!='':
            fdir,fname = os.path.split(attFile)
            att = MIMEText(open(attFile,'rb').read(),'base64','utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment;filename="'+fname+'"'
            msgRoot.attach(att)
       #设定内置图片信息
#        fp = open('test.jpg', 'rb')
#        msgImage = MIMEImage(fp.read())
#        fp.close()
#        msgImage.add_header('Content-ID', '<image1>')
#        msgRoot.attach(msgImage)

       #发送邮件
        smtp = smtplib.SMTP()
       #设定调试级别，依情况而定
        smtp.set_debuglevel(0)
        try:
            smtp.connect(server)
            smtp.login(user, passwd)
            smtp.sendmail(strFrom, strTo, msgRoot.as_string())
            smtp.quit()
            #        smtp.sendmail(strFrom, strTo, msgRoot.as_string())
        except Exception as e:
            msg=e
        if msg:
            return msg
        return 1

