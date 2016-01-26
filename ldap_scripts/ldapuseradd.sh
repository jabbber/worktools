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
dn: cn=$username,ou=aaa,ou=root,dc=example,dc=com
cn: $username
sn: $username
ou: aaa
objectClass: person
objectClass: organizationalPerson
pwdPolicySubentry: cn=Default Policy,dc=example,dc=com
userPassword:
EOF

ldapadd -H $URI -x -D "$admin_dn" -w "$admin_pw" -f $commitfile

rm $commitfile
