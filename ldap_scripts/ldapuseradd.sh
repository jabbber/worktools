#!/bin/bash

#load config
source config.sh
commitfile="/tmp/$$.ldif"

usage="example:\n$0 [USERNAME]"

if [[ $1 = '-h' ]]; then
    echo -e $usage
    exit 1
fi

username=$1

cat >$commitfile <<EOF
dn: uid=$username,ou=root,dc=example,dc=com
cn: $username
ou: root
givenName: $username
objectClass: top
objectClass: posixAccount
objectClass: inetOrgPerson
uid: $username
uidNumber: 1001
gidNumber: 100
sn: root
homeDirectory:
userPassword:
EOF

ldapadd -H $URI -x -D "$admin_dn" -w "$admin_pw" -f $commitfile

rm $commitfile
