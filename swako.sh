#!/bin/sh -eu

if [ ! `which python2.7` ]; then
    echo "Python 2.7 is not installed. Please install and try again."
    exit 1
fi

# Install gyb if not installed
if [ ! -x ./gyb/gyb ]; then
    echo "Attempt to download gyb from GitHub."
    rm -rf gyb
    curl "https://raw.githubusercontent.com/apple/swift/master/utils/gyb.py" -o "gyb/gyb.py"
    curl "https://raw.githubusercontent.com/apple/swift/master/utils/gyb" -o "gyb/gyb"
    chmod +x gyb/gyb
fi