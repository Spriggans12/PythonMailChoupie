# -*- coding: utf-8 -*-
from time import sleep

from tasks.sendFirstMailTask import SendFirstMailTask
from tasks.sendMailsInFolderTask import SendMailsInFolderTask

def main():
    scheduledTasks = [SendFirstMailTask(), SendMailsInFolderTask()]
    # TODO : while True
    for x in range(10):
        for schd in scheduledTasks:
            schd.resolve()
        sleep(0.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
    finally:
        print 'All done'