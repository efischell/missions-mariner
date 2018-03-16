#!/bin/bash

function cruise_info
{
    echo "current cruise is set to: "
    if [[ -e cruise/current ]]; then
        ls -ld cruise/current | sed "s/.*-> //"
    else
        echo "(not set)"
    fi
    echo 
    echo "available cruises include: "
    ls cruise | grep --invert-match current
}

if [ -z "$1" ]; then
    echo "usage: ./cruiseconfig.sh {cruisename}"
    echo
    cruise_info
    exit 1
fi

if [ ! -e "cruise/$1" ]; then
    echo "invalid cruise $1"
    echo 
    cruise_info
    exit 1
fi

cd cruise
rm -f current
ln -s $1 current
cd ..