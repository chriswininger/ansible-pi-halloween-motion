#!/usr/bin/env bash

# runs on the pi where ansible has created a virtual env and copied the app script into the same directory
source /home/chris/ansible-pi-halloween-motion-app/venv/bin/activate
python3 /home/chris/ansible-pi-halloween-motion-app/app.py --no-output
