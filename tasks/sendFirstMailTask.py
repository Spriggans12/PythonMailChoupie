# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from abstractTask import AbstractTask
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

    def check(self):
        return False

    def act(self):
        smtpUtil.sendMail(smtpUtil.createMessage(self.subject, self.body))