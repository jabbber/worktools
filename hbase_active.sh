#!/bin/sh

DEBUG=0

TABLENAME='zabbixtest'

hbshell() {
    if [[ DEBUG -ne 0 ]]; then
        out=`echo $1 | hbase shell -n`
    else
        out=`echo $1 | hbase shell -n 2>/dev/null`
    fi

    status=$?

    if [[ DEBUG -ne 0 ]];then
        echo $out
    fi
    if [[ $status -ne 0 ]]; then
        echo "The command \"$1\" failed."
    else
        echo "The command \"$1\" ok."
    fi
    failed $status
    return $status
}

return_code=''

failed() {
    if [[ $1 -ne 0 ]]; then
        return_code+=1
    else
        return_code+=0
    fi
}

hbshell "list"
hbshell "create '$TABLENAME', 'cf'"
hbshell "put '$TABLENAME', 'row1', 'cf:a', 'value1'"
hbshell "scan '$TABLENAME'"
hbshell "get '$TABLENAME', 'row1'"
hbshell "disable '$TABLENAME'"
hbshell "drop '$TABLENAME'"

echo "Result: $return_code ('1' is failed)"
((return_code=2#$return_code));
exit $return_code
