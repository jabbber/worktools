#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os,sys
import logging
import ConfigParser
import threading
import Queue
import time
import traceback
import signal
from signal import SIGTERM

# Parser config
run_dir = os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))
config_file = os.path.join(run_dir,'ThreadPool.cfg')
cfg = ConfigParser.ConfigParser()
cfg.read(config_file)


logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(name)s [%(process)d] %(levelname)s: %(message)s',
    datefmt=cfg.get('log','datefmt'),
    filename=cfg.get('log','file'),
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
        self.__logger = logging.getLogger('TaskMgr')

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
            self.__logger = logging.getLogger('TaskMgr')
            self.start()

        def run(self):
            while True:
                task = None
                task = self.__taskmgr.getTask()
                if task:
                    try:
                        self.__taskmgr.doJob(task)
                    except:
                        self.__logger.error(traceback.format_exc())

class DaemonMgr:
    def __init__(self,name):
        self.name = name
        global cfg
        self.pidfile = cfg.get('daemon','pid')
        self.pid = None
        self.__logger = logging.getLogger('DaemonMgr')
    def startjob(self):
        pass
    def stopjob(self):
        pass
    def start(self):
        if self.__isAlive(self.__isPID()):
            print 'pid %d, %s is already running'%(self.pid,self.name)
            return True
        pid = os.fork()
        if pid:
            time.sleep(1)
            if not self.__isAlive(self.__isPID()):
                print '%s start failed!'%self.name
                return False
            print "pid %d, %s is started."%(self.__isPID(), self.name)
            return True
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
        work = self.Work(self.startjob)
        while True:
            if not work.isAlive():
                break
            if not self.__keepPID():
                self.__logger.error('can not write %s , %s stop'%(self.pidfile,self.name))
                sys.exit(1)
            time.sleep(1)
        self.__logger.warning('work is finished , %s stop'%self.name)
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
            msg =  "pid %d ,%s is stoped"%(self.pid,self.name)
            self.__logger.info(msg)
            print msg
        else:
            print "%s has been stoped"%self.name
        return True
    def status(self):
        if self.__isAlive(self.__isPID()):
            print "pid %d ,%s is started"%(self.pid,self.name)
            return True
        else:
            if self.pid:
                print "pid %d ,%s is died"%(self.pid,self.name)
            else:
                print "%s not running"%self.name
            return False
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
        if self.__isAlive(self.__isPID()):
            self.__logger.warning('%s is already running'%self.name)
            return False
        else:
            try:
                open(self.pidfile,'w').write(str(os.getpid())+'\n')
                self.__logger.debug('%s is running, %s create'%(self.name,self.pidfile))
                self.__logger.info('%s is started'%self.name)
            except:
                self.__logger.error(traceback.format_exc())
                self.__logger.error("can not write pid to '%s',stop now.")
                return False
        return True
    class Work(threading.Thread):
        def __init__(self,function):
            threading.Thread.__init__(self)
            self.daemon = True
            self.__logger = logging.getLogger('DaemonMgr')
            self.function = function
            self.start()
        def run(self):
            try:
                self.function()
            except:
                self.__logger.error(traceback.format_exc())       

if __name__ == "__main__":
    def usage():
        print 'usage: %s start|stop|status|restart' %sys.argv[0]
    class MyDaemonMgr(DaemonMgr):
        def startjob(self):
            global cfg
            taskmgr = TaskManager(cfg.getint('task','task_max'),cfg.getint('task','thread'))
            for i in range(100):
                taskmgr.putTask(i)
            while True:
                time.sleep(1)

    daemon = MyDaemonMgr('threadpool')
    if len(sys.argv) != 2:
        usage()
    elif sys.argv[1] == 'start':
        if daemon.start(): sys.exit(0)
    elif sys.argv[1] == 'stop':
        if daemon.stop(): sys.exit(0)
    elif sys.argv[1] == 'status':
        if daemon.status(): sys.exit(0)
    elif sys.argv[1] == 'restart':
        if daemon.stop() and daemon.start(): sys.exit(0)
    else: usage()
    sys.exit(1)

