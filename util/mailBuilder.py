# -*- coding: utf-8 -*-
import ConfigParser
from os.path import basename
import glob
import re
import email
import email.header
import email.message
from email.mime.application import MIMEApplication
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# Reads config
config = ConfigParser.RawConfigParser()
config.readfp(open(r'conf/config.ini'))
fromm = config.get('smtp-conf', 'from')
to = config.get('smtp-conf', 'to')

def createMessage(subject, body):
    msg = MIMEMultipart()
    msg['From'] = fromm
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html', _charset="UTF-8"))
    return msg

def getNumberOfMails(folderExtractedInto):
    with open(r'' + folderExtractedInto + '/TOTAL', 'r') as total:
        res=total.read().replace('\n', '')
    return int(res)

def buildMailFromFolder(idMsg, folderExtractedInto):
    print 'Creating message #%s...' %(idMsg)

    with open(r'' + folderExtractedInto + '/' + str(idMsg) + '_HTML.html', 'r') as htmlFile:
        htmlBody=htmlFile.read()

    with open(r'' + folderExtractedInto + '/' + str(idMsg) + '_SUBJECT.txt', 'r') as subjectFile:
        subject=subjectFile.read()

    msg = MIMEMultipart()
    msg['From'] = fromm
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(htmlBody, 'html', _charset="UTF-8"))

    for f in glob.glob(folderExtractedInto + '/' + str(idMsg) + '_ATTACH_*'):
        originalFileName = trimAttachPrefix(basename(f))
        with open(f, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=originalFileName)
        part['Content-Disposition'] = 'attachment; filename="%s"' % originalFileName
        msg.attach(part)
        print ' -> Attached %s to message !' %(originalFileName)

    return msg

def trimAttachPrefix(filename):
    return re.sub('^[0-9]+_ATTACH_', '', filename)