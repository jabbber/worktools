#/bin/bash

#load config
source config.sh
usage="usage:\n\t$0 [OUNAME]"

keyword=$1

if [[ $1 = '-h' ]];then
    echo -e $usage
    exit 1
fi

dnlist=`ldapsearch -H $URI -x -D "$admin_dn" -w "$admin_pw" -b "$searchbase" -LLL ou="$keyword" dn|grep "^dn:"|awk '{ print $2 }'`

if [[ $dnlist = '' ]];then
    echo "not found ou with 'ou=$keyword'"
    exit 2
fi

if echo -e $dnlist|grep -q ".*,ou=$keyword"; then
    echo -e "match dn:\n$dnlist\n"
    echo "Can not delete ou '$keyword'!"
    echo "subordinate objects must be deleted first, quit now."
    exit 3
fi

if [[ $(echo -e "$dnlist"|wc -l) -gt 1 ]];then
    echo -e "match dn:\n$dnlist\n"
    read -p "more then one dn are marched, are you sure? Input 'Yes' to continue:" choice
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

