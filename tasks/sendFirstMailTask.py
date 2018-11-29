# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os.path
from abstractTask import AbstractTask
from util import mailBuilder
from util import smtpUtil
import ConfigParser

class SendFirstMailTask(AbstractTask):
    def __init__(self):
        super(SendFirstMailTask, self).__init__()
        self.initConfig()

    def initConfig(self):
        config = ConfigParser.RawConfigParser()
        config.readfp(open(r'conf/config.ini'))
        self.body = config.get('first-mail-conf', 'body')
        self.subject = config.get('first-mail-conf', 'subject')
        self.fileToCheck = config.get('first-mail-conf', 'checkFile')

    def check(self):
        return os.path.isfile(r'' + self.fileToCheck) 

    def act(self):
        smtpUtil.sendMail(mailBuilder.createMessage(self.subject, self.body))