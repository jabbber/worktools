import os,sys
import time
import traceback
import signal
import thread
from signal import SIGTERM

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
            print('daemon is already running')
            return True
        pid = os.fork()
        if pid:
            def onSigChld(*args):
                pass
            signal.signal(signal.SIGCHLD, onSigChld)
            n = 0 
            while not self.__isPID():
                n += 1
                if n > 100:
                    print('start time out!')
                    sys.exit(self.EXIT_Timeout)
                time.sleep(0.1)
            print('started')
            print "%s has been started."%self.name
            return True
        os.setsid()
        pid = os.fork()
        if pid:
            exit()
        thread.start_new_thread(self.startjob,())
        while True:
            if not self.__keepPID():
                exit()
            time.sleep(1)
    def stop(self):
        if self.__isPID():
            os.kill(self.pid,SIGTERM)
        if self.__isAlive(self.pid):
            return False
        os.unlink(self.pidfile)
        return True
    def status(self):
        if self.__isAlive(self.__isPID()):
            print "pid %d ,daemon is started"%self.pid
        else:
            print "daemon is stoped"
    def __isAlive(self,pid):
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
            print('daemon is already running')
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

    daemon = DaemonMgr('pydaemon')
    if len(sys.argv) != 2:
        usage()
    elif sys.argv[1] == 'start':
        daemon.start()
    elif sys.argv[1] == 'stop':
        daemon.stop()
    elif sys.argv[1] == 'status':
        daemon.status()
    else: usage()
