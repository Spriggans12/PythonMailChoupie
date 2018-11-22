# -*- coding: utf-8 -*-
import ConfigParser
from smtplib import SMTP
from imaplib import IMAP4_SSL
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import email

# Reads config
config = ConfigParser.RawConfigParser()   
config.readfp(open(r'config.ini'))
fromaddr = config.get('my-config', 'fromaddr')
toaddr = config.get('my-config', 'toaddr')
password = config.get('my-config', 'password')
subject = config.get('my-config', 'subject')
body = config.get('my-config', 'body')
folderMessageToForward = config.get('my-config', 'folderMessageToForward')
doSendMail = config.get('my-config', 'doSendMail')
doForwardMail = config.get('my-config', 'doForwardMail')
user = config.get('my-config', 'user')
debug = config.get('my-config', 'debug')


# Sends message
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain', _charset='utf-8'))

server = SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(user, password)

if debug == 'y':
    print 'Destination :', toaddr
    print 'Sending from :', fromaddr
    print 'Subject :', subject
    print 'Content :'
    print '-------------'
    print body
    print '-------------'
    print

if doSendMail == 'y':
    print '=> Sending mail...'
    server.sendmail(fromaddr, toaddr, msg.as_string())
    print '=> ...Done !'
else:
    print '=> Mail was not sent because it has been disabled.'
server.quit()

# Forwards message in the asked folder
client = IMAP4_SSL('imap.gmail.com')
client.login(user, password)

# Lists available imap folders
if debug == 'y':
    for folder in client.list()[1]:
        print folder

# Fetches the message data
client.select(folderMessageToForward)
status, data = client.fetch(1, '(RFC822)')
email_data = data[0][1]
client.close()
client.logout()
# create a Message instance from the email data
fwdMsg = email.message_from_string(email_data)
# replace headers (could do other processing here)
fwdMsg.replace_header("From", fromaddr)
fwdMsg.replace_header("To", toaddr)

# Sends forwarded mail
server = SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.login(user, password)

if doForwardMail == 'y':
    print '=> Forwarding mail...'
    server.sendmail(fromaddr, toaddr, fwdMsg.as_string())
    print '=> ...Done !'
else:
    print '=> Mail was not sent because it has been disabled.'
server.quit()