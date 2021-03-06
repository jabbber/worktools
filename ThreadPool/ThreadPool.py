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
import uuid

# Parser config
run_dir = os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))
config_file = os.path.join(run_dir,'ThreadPool.cfg')
cfg = ConfigParser.ConfigParser()
cfg.read(config_file)

loglevel = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR
    }

logging.basicConfig(level=loglevel[cfg.get('log','level')],
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
        self.__threads = {}
        self.idel = {}
        self.working = {}
        self.__logger = logging.getLogger('TaskMgr')

        self.initThreads()
    
    def initThreads(self):
        for i in range(self.__maxThreads):
            try:
                self.__threads[i] = self.Work(i,self)
            except:
                self.__logger.warning(traceback.format_exc())
                self.__logger.warning("can not create more than %d threads!"%i)
                break
    
    def getTask(self):
        return self.__taskQueue.get();

    def putTask(self,task):
        while self.__taskQueue.full():
            self.__logger.warning("task queue full, retry")
            time.sleep(1)
        self.__taskQueue.put(task)
        return True

    def doJob(self,task):
        '''overload to do work'''
        self.__logger.debug("%s"%task)

    def getQsize(self):
        return self.__taskQueue.qsize()

    class Work(threading.Thread):
        def __init__(self,name,taskmgr):
            threading.Thread.__init__(self)
            self.name = name
            self.daemon = True
            self.__task = None
            self.__taskmgr = taskmgr
            self.__logger = logging.getLogger('TaskMgr.Work(%s)'%self.name)
            self.start()

        def run(self):
            while True:
                self.__task = None
                self.__taskmgr.idel[self.name] = ''
                self.__task = self.__taskmgr.getTask()
                if self.__task:
                    taskID = uuid.uuid4()
                    self.__taskmgr.idel.pop(self.name)
                    self.__taskmgr.working[self.name] = taskID
                    self.__logger.debug('task %s begin'%taskID)
                    try:
                        self.__taskmgr.doJob(self.__task)
                    except:
                        self.__logger.error(traceback.format_exc())
                    self.__taskmgr.working.pop(self.name)
                    self.__logger.debug('task %s end'%taskID)
        def idel(self):
            if self.__task:
                return True
            return False

class DaemonMgr:
    def __init__(self,name):
        self.name = name
        global cfg
        self.pidfile = cfg.get('daemon','pid')
        self.pid = None
        self.__logger = logging.getLogger('DaemonMgr')
    def startjob(self):
        '''overload to run main process'''
        pass
    def stopjob(self):
        '''overload to stop main process'''
        pass
    def stopHander(self,signum, frame):
        try:
            self.stopjob()
        except:
            self.__logger.error(traceback.format_exc())
            self.__logger.error("can not stop program savely ,stop force now.")
        msg = "%s is stoped by signal %s."%(self.name, signum)
        self.__logger.warning(msg)
        sys.exit(0)

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
        signal.signal(signal.SIGTERM, self.stopHander)
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
                os.kill(self.pid,signal.SIGTERM)
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
                self.__logger.warning('%s is started'%self.name)
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
    # over task and daemon manager to do some work
    class MyTaskMgr(TaskManager):
        def doJob(self,task):
            logger = logging.getLogger('TaskMgr.Work')
            time.sleep(task)
            logger.debug('sleep %d seconds'%task)
    class MyDaemonMgr(DaemonMgr):
        def startjob(self):
            logger = logging.getLogger('TaskMgr')
            global cfg
            taskmgr = MyTaskMgr(cfg.getint('task','task_max'),cfg.getint('task','thread_max'))
            import random
            n = 0
            while True:
                logger.info("task queue size %d."%taskmgr.getQsize())
                logger.info("thread idel %d"%len(taskmgr.idel))
                logger.info("thread working %d"%len(taskmgr.working))
                for i in range(random.randint(10,50)):
                    taskmgr.putTask(random.randint(1,10))
                    n += 1
                logger.info("task insert '%d'"%n)
                time.sleep(1)
        def stopjob(self):
            pass

    daemon = MyDaemonMgr('threadpool')
    def usage():
        print 'usage: %s start|stop|status|restart' %sys.argv[0]
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

