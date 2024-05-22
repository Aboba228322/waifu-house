#!/bin/sh

python main.py &
python webhook_server.py &

wait