#!/usr/bin/env bash

set -e

if [[ ${#} != 1 ]]; then
    echo "USAGE: ./ssh_run.sh pi@192.168.10.10"
    exit
fi

APP_NAME=btc-register
DEST=${1}

./rsync.sh ${DEST}

# Run the script on the remote Raspberry Pi.
# `-t`:  Force pseudo-tty allocation to get remote terminal outputs colored.
ssh -t ${DEST} "cd ${APP_NAME}; bash ./run.sh"
