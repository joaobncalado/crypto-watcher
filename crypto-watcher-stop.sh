#!/bin/bash

APP_ID=$(ps -C main.py --no-header --format 'pid')

if [ -n "${APP_ID}" ]; then
    sudo kill ${APP_ID}
fi

