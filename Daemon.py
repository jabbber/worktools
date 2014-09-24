import os
import traceback
import signal

class Daemon:
    EXIT_OK,EXIT_AlreadyRun,EXIT_PIDWriteError,EXIT_Timeout = range(4)
    def self.__init__(self,name,logfile=None,errorfile=None):
        self.logfile = logfile
        self.errorfile = errorfile
        self.name = name
        self.pidfile = '/var/run/%s'%name
    def self.startjob(self):
        pass
    def self.stopjob(self):
        pass
    def self.start(self):
        if self.__isDaemon():
            print('daemon is already running,stop now.')
            sys.exit(self.EXIT_AlreadyRun)
        pid = os.fork()
        if pid:
            def onSigChld(*args):
                print *args
                print('start fail!')
                sys.exit(9)
            signal.signal(signal.SIGCHLD, onSigChld)
            n = 0 
            while not self.isDaemon()
                n += 1
                if n > 100:
                    print('start time out!')
                    sys.exit(self.EXIT_Timeout)
                time.sleep(0.1)
            print('started')
            sys.exit(self.EXIT_OK)
        os.setsid()
        devnull = os.open('/dev/null',os.O_RDWR)
        os.dup2(devnull,0)
        os.close(devnull)
        del devnull
        if self.logfile:
            logop = open(self.logfile,'a',1)
            os.dup2(logop.fileno(),1)
        if self.errorfile:
            errorop = open(self.errorfile,'a',1)
            os.dup2(errorop.fileno(),2)
            del errorop
        else if logop:
            os.dup2(logop.fileno(),2)
        if logop:
            del logop
        print "%s has been started."%self.name
        thread.start_new_thread(self.startjob())
    def self.stop(self):
        pass
    def __isAlive(self,pid):
        if os.path.isdir('/proc/%d'%pid):
            return True
        else:
            return False
    def __isDaemon(self):
        if os.path.isfile(pidfile):
            try:
                pid = int(open(pidfile).read().strip())
            except:
                pid = None
            if pid:
                if self.__isAlive(pid):
                    return True
        return False
    def __keepPid(self):
        if os.path.isfile(self.pidfile):
            try:
                pid = int(open(pidfile).read().strip())
            except:
                pid = None
        if pid:
            if os.getpid() == pid:
                return 0
            else:
                if self.__isDaemon():
                    print('daemon is already running,stop now.')
                    sys.exit(self.EXIT_AlreadyRun)
        try:
            open(pidfile,'w').write(str(os.getpid())+'\n')
        except:
            print(traceback.print_exc())
            print("can not write pid to '%s',stop now.")
            sys.exit(self.EXIT_PIDWriteError)
