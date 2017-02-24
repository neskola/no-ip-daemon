#!/bin/bash -

echo "Kill existing pid and remove daemon pid -files in /tmp/"

pid=$(pgrep -f "no-ip-daemon.py")

if [[ $pid = *[[:digit:]]* ]]; then
    echo "Found process with pid ("$pid"). Killing it."
    kill -9 $pid
    rm /tmp/no-ip-daemon.pid
fi

cd /opt/no-ip-daemon
python no-ip-daemon.py

while pgrep -u root -f "no-ip-daemon.py" > /dev/null; do sleep 1; done

