#!/usr/bin/env bash

export APP_HOME="${HOME}/.btc-register"
export KIVY_HOME="${HOME}/.btc-register/kivy"
export KIVY_GL_BACKEND='gl'  # [issue #6007](https://github.com/kivy/kivy/issues/6007)

BASE_DIR=$(cd $(dirname $0); pwd)
RESTART_FILE="${APP_HOME}/.restart"

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
