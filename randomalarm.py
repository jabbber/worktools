#!/usr/bin/env python3
import sys
import re
from time import localtime
from random import randint

#time_filter = (('date1',re.compile('201\d(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1])')),
#    ('date2',re.compile('201\d-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1,2][0-9]|3[0,1])')),
#    ('date3',re.compile('(?:0[1-9]|1[0-2])/(?:0[1-9]|[1,2][0-9]|3[0,1])/201\d')),
#    ('time1',re.compile('(?:[0,1][0-9]|2[0-3])(?:[0-5][0-9]){2}')),
#    ('time2',re.compile('(?:[0,1][0-9]|2[0-3])(?:\:[0-5][0-9]){2}')))

time1 = re.compile('(?:[0,1][0-9]|2[0-3])(?:\:[0-5][0-9]){2}')
def time_format(date,time):
    return { '{date0}':date,
    '{time0}':time,
    '{date1}':date[:4] + '-'+date[4:6] + '-' + date[6:],
    '{date2}':date[4:6] + '/' + date[6:] + '/' + date[:4],
    '{time1}':time[:2] + ':' + time[2:4] + ':' + time[4:],
    }
def gettime(seconds):
    (tm_year,tm_mon,tm_mday,tm_hour,tm_min,tm_sec,tm_wday,tm_yday,tm_isdst) = localtime(seconds)
    return ('{:04d}{:02d}{:02d}'.format(tm_year,tm_mon,tm_mday),'{:02d}{:02d}{:02d}'.format(tm_hour,tm_min,tm_sec))

alarm_list = []
with open(sys.argv[1],encoding='gb18030') as f:
    for line in f:
        col = line.split('\t')
        date = col[3]
        time = col[4]
        time_place = time_format(date,time)
        for place in time_place:
            line = line.replace(time_place[place],place)
        line = re.sub(time1,'{time1}',line)
        alarm_list.append(line)

alarm_max = len(alarm_list) - 1
num = 0
for stime in range(1361203200,1366041600,86400):
    n = randint(30,100)
    while n > 0:
        n -= 1
        num += 1
        time_place = time_format(*gettime(stime+randint(0,86399)))
        print(alarm_list[randint(0,alarm_max)].format(date0=time_place['{date0}'],
            date1=time_place['{date1}'],
            date2=time_place['{date2}'],
            time0=time_place['{time0}'],
            time1=time_place['{time1}']),end='')
        print('line:{}'.format(num),end='\r',file=sys.stderr)
print('line:{}'.format(num),file=sys.stderr)
