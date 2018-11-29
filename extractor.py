# -*- coding: utf-8 -*-
import sys
import imaplib
import ConfigParser
from util import smtpUtil
import email
import email.header
import shutil
import os

config = ConfigParser.RawConfigParser()
config.readfp(open(r'conf/config.ini'))
user = config.get('smtp-conf', 'user')
password = config.get('smtp-conf', 'password')
folderMessageToForward = config.get('extractor-conf', 'folderMessageToForward')
outputDirectory = config.get('extractor-conf', 'outputDirectory')

def cleanFolder():
    print 'Deleting and creating folder', outputDirectory
    shutil.rmtree(outputDirectory, ignore_errors=True)
    os.mkdir(outputDirectory)
    print 'Done !'

def process_mailbox(imap):
    rv, data = imap.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return
    # Email extraction
    for num in data[0].split():
        rv, data = imap.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return
        print '----'
        print "Reading message number", num
        mail = email.message_from_string(data[0][1])
        if mail.is_multipart():
            for part in mail.walk():
                ctype = part.get_content_type()
                #print ctype
                if ctype in ['image/jpeg', 'image/png', 'application/pdf']:
                    open('%s/%s_ATTACH_%s' %(outputDirectory, num, part.get_filename()), 'wb').write(part.get_payload(decode=True))
                    print 'Added', part.get_filename()
                elif ctype == 'text/html':
                    open('%s/%s_HTML.html' %(outputDirectory, num), 'wb').write(part.get_payload(decode=True))
                    print 'Added HTML'
        else:
            print 'Not a multipart mail ! Cannot be extracted !'
        open('%s/%s_SUBJECT.txt' %(outputDirectory, num), 'wb').write(email.header.decode_header(mail['Subject'])[0][0])
    open('%s/TOTAL' %(outputDirectory), 'wb').write(str(len(data[0])))

def main():
    cleanFolder()
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(user, password)
    rv, data = imap.select(folderMessageToForward)
    if rv == 'OK':
        print "Processing mailbox: ", folderMessageToForward
        process_mailbox(imap)
        imap.close()
    else:
        print "ERROR: Unable to open mailbox ", rv
    imap.logout()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
    finally:
        print 'All done'