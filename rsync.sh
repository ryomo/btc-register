#!/usr/bin/env bash

set -e

if [[ ${#} != 1 ]]; then
    echo "USAGE: ./rsync.sh pi@192.168.10.10"
    exit
fi

APP_NAME=btc-register
DEST=${1}

# Note: Directory may not be deleted automatically if it is written on `.rsyncignore`.
rsync -ahvc --delete --exclude-from=.rsyncignore ./ ${DEST}:/home/pi/${APP_NAME}

rsync -ahvc config/kivy_config.ini ${DEST}:/home/pi/.${APP_NAME}/kivy/config.ini

date
