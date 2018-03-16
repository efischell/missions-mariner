#!/bin/bash

function array_info
{
    echo "current array is set to: "
    ls -ld array_plugs | sed "s/.*-> //" | sed "s#.*/arrays/##"
    echo 
    echo "available arrays include: "
    ls ../arrays
}

if [ -z "$1" ]; then
    echo "usage: ./array_config.sh {arrayname}"
    echo
    array_info
    exit 1
fi

if [ ! -e "../arrays/$1" ]; then
    echo "invalid array $1"
    echo 
    array_info
    exit 1
fi

rm -f array_plugs
ln -s ../arrays/$1 array_plugs
