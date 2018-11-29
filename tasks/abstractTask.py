# -*- coding: utf-8 -*-
class AbstractTask(object):
    def __init__(self):
        self.done = False

    def resolve(self):
        if self.done:
            return False
        if self.check() == True:
            self.act()
            self.done = True
            return True
        return False

    def check(self):
        raise NotImplementedError("Please Implement this method")

    def act(self):
        raise NotImplementedError("Please Implement this method")