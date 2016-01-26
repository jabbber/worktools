#!/bin/bash

#load config
source config.sh
commitfile="/tmp/$$.ldif"

usage="example:\n$0 [OUNAME]"

if [[ $1 = '-h' ]]; then
    echo -e $usage
    exit 1
fi

ouname=$1

cat >$commitfile <<EOF
dn: ou=$ouname,ou=root,dc=example,dc=com
objectClass: organizationalUnit
ou: $ouname

EOF

ldapadd -H $URI -x -D "$admin_dn" -w "$admin_pw" -f $commitfile

rm $commitfile
