# -*- coding: utf-8 -*-
import ConfigParser
import email
import email.header
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from smtplib import SMTP

# Reads config
config = ConfigParser.RawConfigParser()
config.readfp(open(r'conf/config.ini'))
fromm = config.get('smtp-conf', 'from')
to = config.get('smtp-conf', 'to')
user = config.get('smtp-conf', 'user')
password = config.get('smtp-conf', 'password')
doSendMails = config.get('smtp-conf', 'doSendMails')

def sendMail(msg):
    smtp = SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(user, password)
    if doSendMails == 'y':
        print '=> Sending mail to', email.header.decode_header(msg['To'])[0][0] ,'...'
        smtp.sendmail(fromm, to, msg.as_string())
        print '=> ...Done !'
    else:
        print '=> Mail was not sent because sending it has been disabled.'
    smtp.quit()
