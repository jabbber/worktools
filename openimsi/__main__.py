#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os,sys
import openimsi

HOST_LIST = 'hostlist'
BLACK_LIST = 'blacklist'
SOURCE_DIR = 'src'
DIST_DIR = 'target'
OUT_TYPE = 'xlsx'

def we_are_frozen():
    """Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located."""

    return hasattr(sys, "frozen")

def module_path():
    """ This will get us the program's directory,
    even if we are frozen using py2exe"""

    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))
    
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))
#    return os.path.split(os.path.realpath(unicode(__file__, sys.getfilesystemencoding( ))))[0]    

def convert(run_dir,src_dir,dist_dir):
    print 'Start convert %s:'%src_dir
    for file_name in os.listdir(src_dir):
        if os.path.isdir("%s/%s"%(src_dir, file_name)):
            pass
        else:
            name,ext = os.path.splitext(file_name)
            print "convert %s%s"%(name,ext)
            output_file = '%s/%s'%(dist_dir,name)
            t.clear()
            result = t.load('%s/%s'%(src_dir, file_name))
            if result:
                if OUT_TYPE == 'html':
                    open(output_file + '.html', 'w').write(t.get_html('all'))

                elif OUT_TYPE == 'xlsx':
                    t.get_xlsx(output_file +'.xlsx')

    print 'Convert %s Complite!\n'%src_dir
    return 0

if __name__ == '__main__':
    #初始化转换器参数
#    run_dir = os.path.split(os.path.realpath(__file__))[0]
    run_dir = os.path.realpath(module_path())
    print run_dir
    t = openimsi.Tables()

    host_list = '%s/%s'%(run_dir,HOST_LIST)
    for ext in ('.txt','.xlsx'):
        if os.path.isfile(host_list + ext):
            print "load Host List from %s%s"%(host_list,ext)
            t.hostlist = t.load_list(host_list + ext)
            break

    if t.hostlist == []:
        print 'Please give a useful hostlist file like hostlist.txt or hostlist.xlsx in script dir!'
        raw_input("Press Enter to Exit. ")
        sys.exit(1)

    black_list = '%s/%s'%(run_dir,BLACK_LIST)
    for ext in ('.txt','.xlsx'):
        if os.path.isfile(black_list + ext):
            print "load Black List from %s%s"%(black_list,ext)
            t.blacklist = t.load_list(black_list + ext)
            break

    #获得输入输出目录
    work_dirs = []
    for value in os.listdir(run_dir):
        src_dir = "%s/%s"%(run_dir,value)
        if os.path.isdir(src_dir) and value[0] != '.':
            dist_dir = "%s/%s"%(src_dir,DIST_DIR)
            if os.path.isdir(dist_dir):
                print "skip %s"%src_dir

            elif os.path.isfile("%s/__init__.py"%src_dir):
                print "skip %s"%src_dir

            else:
                work_dirs.append([src_dir, dist_dir])
                print "%s will be convert"%src_dir

#    if raw_input("\nPress Enter to Continue ") == '':
    for work_dir in work_dirs:
            os.mkdir(work_dir[1])
            convert(run_dir,work_dir[0],work_dir[1])

#    else:
#        exit()

    print 'All dir convert Complite!\n'
    raw_input("Press Enter to Exit. ")

