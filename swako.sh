#!/bin/sh -eu

#############################
# Functions

function showHelp() {
    echo "usage: $ swako generate [gyb] [output]"
}

#############################

if [ ! `which python2.7` ]; then
    echo "Python 2.7 is not installed. Please install and try again."
    exit 1
fi

# Install gyb if not installed
if [ ! -x ./gyb/gyb ]; then
    echo "Attempt to download gyb from GitHub."
    rm -rf gyb
    mkdir gyb
    curl "https://raw.githubusercontent.com/apple/swift/master/utils/gyb.py" -o "gyb/gyb.py"
    curl "https://raw.githubusercontent.com/apple/swift/master/utils/gyb" -o "gyb/gyb"
    chmod +x gyb/gyb
fi

if [ $# = 0 ]; then
    subcommand="help"
else
    subcommand=$1
fi

case $subcommand in
    "help" )
        showHelp
        ;;
    "generate" )
        gybName=$2
        outputName=$3
        ./gyb/gyb $gybName -o $outputName --line-directive=
        ;;
esac
