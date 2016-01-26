#/bin/bash

#load config
source config.sh
usage="usage:\n\t$0 disable [USERNAME]\n\t$0 enable [USERNAME]"

action=$1
keyword=$2
commitfile="/tmp/$$.ldif"

if [[ $# -ne 2 ]];then
    echo -e $usage
    exit 1
fi

case $action in
    "enable")
    ;;
    "disable")
    ;;
    *)
    echo -e $usage
    exit 1
    ;;
esac

dnlist=`ldapsearch -H $URI -x -D "$admin_dn" -w "$admin_pw" -b "$searchbase" -LLL cn="$keyword" dn|grep "^dn:"|awk '{ print $2 }'`

if [[ $dnlist = "" ]];then
    echo "not found user with 'cn=$keyword'"
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
    case $action in
        "enable")
            cat >$commitfile <<EOF
dn: $dn
delete: pwdAccountLockedTime
EOF
        ;;
        "disable")
            cat >$commitfile <<EOF
dn: $dn
add: pwdAccountLockedTime
pwdAccountLockedTime: 000001010000Z
EOF
        ;;
        *)
            echo -e $usage
            exit 1
        ;;
    esac
    
    ldapmodify -H $URI -x -D "$admin_dn" -w "$admin_pw" -f $commitfile
    rm $commitfile
done

