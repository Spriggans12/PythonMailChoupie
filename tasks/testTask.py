# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
from abstractTask import AbstractTask
from util import testUtil

class TestTask(AbstractTask):
    def __init__(self):
        super(TestTask, self).__init__()

    def check(self):
        return True

    def act(self):
        testUtil.act()