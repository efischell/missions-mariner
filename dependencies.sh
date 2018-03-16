#!/bin/bash
#
# author: Ian Katz <ijk5@mit.edu>
#
# run make, using DEPENDENCIES as input
# force single job, and use -- to prevent any further options
# command line arguments are interpreted as targets

if [[ $UID -ne 0 ]]; then
    printf "You must run this script as root. Use 'sudo' in Ubuntu. \n" 1>&2
    exit 1
fi

if [[ `lsb_release -is` != "Ubuntu" ]]; then
    printf "This script only works on Ubuntu. Please examine the DEPENDENCIES file as a starting point for finding the required packages on your distribution"
    exit 1
fi

make -j1 -f DEPENDENCIES -- `lsb_release -cs` "$@" 
