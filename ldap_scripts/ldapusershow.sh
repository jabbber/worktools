#!/bin/bash

#load config
source config.sh

usage="example:\n$0 uid=[USERNAME]"

if [[ $1 = '-h' ]]; then
    echo -e $usage
    exit 1
fi

keyword=$1

ldapsearch -H $URI -x -D "$admin_dn" -w "$admin_pw" -b "$searchbase" "$keyword" "*" "+"
