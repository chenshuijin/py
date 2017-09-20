#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'chenshuijin'

import smtplib

from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.163.com"
mail_user = ""
mail_pass = ""

sender = 'xxxx@163.com'
receivers = ['xxxxx@qq.com'] # receiver, can be your qq email address

# three argvs :
#   text: the email text contain
#   plain: the plain
#   encoding: the encoding

message = MIMEText('Python email sender testing...', 'plain', 'utf-8')
message['From'] = Header("teching", 'utf-8')
message['To'] = Header("testing", 'utf-8')

subject = 'Python SMTP email testing'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP('localhost')
#    smtpObj.connect(mail_host, 25)
#    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print 'send email success'
except smtplib.SMTPException:
    print "error: fail to send email"
