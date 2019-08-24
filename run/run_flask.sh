#!/bin/bash

./set-up-db.sh

export FLASK_APP=../src/app.py
export FLASK_ENV=development
export FLASK_RUN_PORT=5000
export FLASK_DEBUG=1

flask run
