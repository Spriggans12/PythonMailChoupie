# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from abstractTask import AbstractTask
from util import smtpUtil
import ConfigParser

class ForwardMailsInFolderTask(AbstractTask):
    def __init__(self):
        super(ForwardMailsInFolderTask, self).__init__()
        self.initConfig()

    def initConfig(self):
        config = ConfigParser.RawConfigParser()
        config.readfp(open(r'conf/config.ini'))
        self.folderMessageToForward = config.get('forward-mail-conf', 'folderMessageToForward')

    def check(self):
        return True

    def act(self):
        smtpUtil.forwardMails(self.folderMessageToForward)