#!/usr/bin/env bash

set -e

if [[ ${#} != 1 ]]; then
    echo "USAGE: ./rsync.sh pi@192.168.10.10"
    exit
fi

APP_PATH='~/btc-register'
APP_HOME='~/.btc-register'
KIVY_HOME='~/.btc-register/kivy'
DEST=${1}

# Note: Directory may not be deleted automatically if it is written on `.rsyncignore`.
rsync -ahvc --delete --exclude-from=.rsyncignore ./ ${DEST}:${APP_PATH}

rsync -ahvc config/kivy_default.ini ${DEST}:${KIVY_HOME}/config.ini

date
