#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import logging
import threading
import Queue
import os,sys
import time
import traceback
import signal
from signal import SIGTERM

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s [%(filename)s line:%(lineno)d] %(levelname)s: %(message)s',
    datefmt='%b %d %Y %H:%M:%S',
    filename='threadPool.log',
    filemode='a')

console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

class TaskManager:
    def __init__(self,maxTasks,maxThreads):
        self.__maxTasks = maxTasks
        self.__maxThreads = maxThreads
        self.__taskQueue = Queue.Queue(maxTasks)
        self.__threads = []
        self.__logger = logging.getLogger('ThreadPool')

        self.initThreads()
    
    def initThreads(self):
        for i in range(self.__maxThreads):
            self.__threads.append(self.Work(self))
    
    def getTask(self):
        return self.__taskQueue.get();

    def putTask(self,task):
        if self.__taskQueue.full():
            return False
        self.__taskQueue.put(task)
        return True

    def doJob(self,task):
        #overload to do work
        self.__logger.debug("%s"%task)

    class Work(threading.Thread):
        def __init__(self,taskmgr):
            threading.Thread.__init__(self)
            self.daemon = True
            self.__taskmgr = taskmgr
            self.start()

        def run(self):
            while True:
                task = None
                task = self.__taskmgr.getTask()
                if task:
                    self.__taskmgr.doJob(task)

class DaemonMgr:
    def __init__(self,name):
        self.name = name
        self.pidfile = '/tmp/%s.pid'%name
        self.pid = None
    def startjob(self):
        pass
    def stopjob(self):
        pass
    def start(self):
        if self.__isAlive(self.__isPID()):
            print('pid %d, %s is already running'%(self.pid,self.name))
            return True
        pid = os.fork()
        if pid:
            n = 0 
            while not self.__isPID():
                n += 1
                if n > 100:
                    print('start time out!')
                    sys.exit(1)
                time.sleep(0.1)
            print "pid %d, %s has been started."%(self.pid, self.name)
            sys.exit(0)
        os.chdir("/")
        os.setsid()
        os.umask(0)
        pid = os.fork()
        if pid:
            exit()
        sys.stdout.flush()
        sys.stderr.flush()
        si = file("/dev/null", 'r')
        so = file("/dev/null", 'a+')
        se = file("/dev/null", 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        self.startjob()
        while True:
            if not self.__keepPID():
                sys.exit(1)
            time.sleep(1)
    def stop(self):
        if self.__isPID():
            if self.__isAlive(self.pid):
                os.kill(self.pid,SIGTERM)
                n = 0
                while self.__isAlive(self.pid):
                    n += 1
                    if n > 100:
                        print "pid %d ,%s stoped failed."%(self.pid,self.name)
                        return False
                    time.sleep(0.1)
            os.unlink(self.pidfile)
            print "pid %d ,%s is stoped"%(self.pid,self.name)
        else:
            print "%s has been stoped"%self.name
        return True
    def status(self):
        if self.__isAlive(self.__isPID()):
            print "pid %d ,%s is started"%(self.pid,self.name)
        else:
            print "%s is stoped"%self.name
    def __isAlive(self,pid,timeout=0):
        if type(pid) == int:
            if os.path.isdir('/proc/%d'%pid):
                return True
        return False
    def __isPID(self):
        if os.path.isfile(self.pidfile):
            try:
                self.pid = int(open(self.pidfile).read().strip())
            except:
                print(traceback.print_exc())
                self.pid = None
            return self.pid
        return False
    def __keepPID(self):
        if self.__isPID() and os.getpid() == self.__isPID():
            return True
        if self.__isAlive(self.pid):
            print('%s is already running'%self.name)
            return False
        else:
            try:
                open(self.pidfile,'w').write(str(os.getpid())+'\n')
            except:
                print(traceback.print_exc())
                print("can not write pid to '%s',stop now.")
                return False
        return True

if __name__ == "__main__":
    def usage():
        print 'usage: %s start|stop|status' %sys.argv[0]
    class MyDaemonMgr(DaemonMgr):
        def startjob(self):
            taskmgr = TaskManager(100,10)
            for i in (1,2,3,4,5,6,7):
                taskmgr.putTask(i)

    daemon = MyDaemonMgr('threadpool')
    if len(sys.argv) != 2:
        usage()
    elif sys.argv[1] == 'start':
        daemon.start()
    elif sys.argv[1] == 'stop':
        daemon.stop()
    elif sys.argv[1] == 'status':
        daemon.status()
    else: usage()
