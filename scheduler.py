# -*- coding: utf-8 -*-
from time import sleep

from tasks.sendFirstMailTask import SendFirstMailTask
from tasks.sendMailsInFolderTask import SendMailsInFolderTask

def main():
    scheduledTasks = [SendFirstMailTask(), SendMailsInFolderTask()]
    tasksCount = 0
    tasksTotal = len(scheduledTasks)
    while tasksCount != tasksTotal:
        for tsk in scheduledTasks:
            if(tsk.resolve() == True):
                tasksCount += 1
        sleep(0.5)
    print 'All tasks are done !'

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
    finally:
        print 'All done'