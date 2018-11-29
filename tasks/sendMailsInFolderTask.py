# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from abstractTask import AbstractTask
from util import mailBuilder
from util import smtpUtil
import ConfigParser

class SendMailsInFolderTask(AbstractTask):
    def __init__(self):
        super(SendMailsInFolderTask, self).__init__()
        self.initConfig()

    def initConfig(self):
        config = ConfigParser.RawConfigParser()
        config.readfp(open(r'conf/config.ini'))
        self.folderExtractedInto = config.get('extractor-conf', 'outputDirectory')

    def check(self):
        return False

    def act(self):
        for idMsg in range(mailBuilder.getNumberOfMails(self.folderExtractedInto)):
            msg = mailBuilder.buildMailFromFolder(idMsg + 1, self.folderExtractedInto)
            smtpUtil.sendMail(msg)