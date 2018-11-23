# -*- coding: utf-8 -*-
import ConfigParser
import email
import email.header
import email.message
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from smtplib import SMTP
from imaplib import IMAP4_SSL

# Reads config
config = ConfigParser.RawConfigParser()
config.readfp(open(r'conf/config.ini'))
fromm = config.get('smtp-conf', 'from')
to = config.get('smtp-conf', 'to')
user = config.get('smtp-conf', 'user')
password = config.get('smtp-conf', 'password')
doSendMails = config.get('smtp-conf', 'doSendMails')

def createMessage(subject, body):
    msg = MIMEMultipart()
    msg['From'] = fromm
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', _charset="UTF-8"))
    return msg

def sendMail(msg):
    smtp = SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(user, password)
    if doSendMails == 'y':
        print '=> Sending mail to', email.header.decode_header(msg['To'])[0] ,'...'
        print msg.as_string()
        smtp.sendmail(fromm, to, msg.as_string())
        print '=> ...Done !'
    else:
        print '=> Mail was not sent because sending it has been disabled.'
        print '------------'
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = decode[0]
        print subject
        print '------------'
    smtp.quit()

def forwardMails(folderToForward):
    imap = IMAP4_SSL('imap.gmail.com')
    imap.login(user, password)
    # Gets inside the specified folder
    imap.select(folderToForward)
    rv, data = imap.search(None, "ALL")
    # Loops through every mail
    for msgId in data[0].split():
        status, mailFetchData = imap.fetch(3, '(RFC822)')
        # Creates a Message instance from the email data
        fwdMsg = email.message_from_string(mailFetchData[0][1])
        # replace headers (could do other processing here)
        fwdMsg.replace_header("To", to)
        fwdMsg.replace_header("From", fromm)
        # Sends this very mail
        sendMail(fwdMsg)
        return
    imap.close()
    imap.logout()