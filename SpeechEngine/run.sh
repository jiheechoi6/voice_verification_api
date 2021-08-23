#!/bin/bash
cd /home/SpeechEngine
source env/bin/activate
service redis-server start
redis-server --daemonize yes
python3 manage.py runserver 172.19.0.2:3000