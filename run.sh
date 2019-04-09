#!/usr/bin/env bash

export APP_HOME='~/.btc-register'
export KIVY_HOME='~/.btc-register/kivy'
export KIVY_GL_BACKEND='gl'  # [issue #6007](https://github.com/kivy/kivy/issues/6007)

BASE_DIR=$(cd $(dirname $0); pwd)
RESTART_FILE="${APP_HOME}/.restart"

# config file
mkdir -p ${APP_HOME}
mkdir -p ${KIVY_HOME}
if [[ ! -f ${KIVY_HOME}/config.ini ]]; then
    cp ${BASE_DIR}/config/kivy_default.ini ${KIVY_HOME}/config.ini
fi

# Restart run.py if `.restart` file exists.
enable_loop=true
while ${enable_loop}
do
    if [[ -f ${RESTART_FILE} ]]; then
        rm ${RESTART_FILE}
    fi

    python3 ${BASE_DIR}/run.py

    if [[ ! -f ${RESTART_FILE} ]]; then
        enable_loop=false
    fi
done
