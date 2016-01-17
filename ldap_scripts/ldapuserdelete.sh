#/bin/bash

#load config
source config.sh
usage="usage:\n\t$0 [USERNAME]"

keyword=$1

if [[ $1 = '-h' ]];then
    echo -e $usage
    exit 1
fi

dnlist=`ldapsearch -H $URI -x -D "$admin_dn" -w "$admin_pw" -b "$searchbase" -LLL uid="$keyword" dn|grep "^dn:"|awk '{ print $2 }'`

if [[ $dnlist = '' ]];then
    echo "not found user with 'uid=$keyword'"
fi

if [[ $(echo -e "$dnlist"|wc -l) -gt 1 ]];then
    echo -e "match dn:\n$dnlist\n"
    read -p "more then one dn are marched, are you sure? print 'Yes' to continue:" choice
    if [[ $choice != 'Yes' ]];then
        exit 0
    fi
fi

IFS=$'\n'
for dn in $dnlist
do
    ldapdelete -H $URI -x -D "$admin_dn" -w "$admin_pw" $dn
    if [[ $? = 0 ]];then
        echo dn: $dn delete successed.
    fi
done

