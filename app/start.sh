#!/usr/bin/env bash

# runs on the pi where ansible has created a virtual env and copied the app script into the same directory
source ./venv/bin/activate
python3 ./app.py --no-output
