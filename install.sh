#!/bin/bash -
if [ "$(id -u)" != "0" ]; then
    echo "Sorry, you are not root. Run as root or use sudo."
    exit 1
fi

cp noip.service /lib/systemd/system/ && chmod 644 /lib/systemd/system/noip.service

installdir="/opt/no-ip-daemon"

if [ ! -d "$installdir" ]; then
    echo "Creating "$installdir" directory"
    mkdir $installdir
fi

cp launcher.sh settings.json no-ip-daemon.py $installdir

systemctl daemon-reload
systemctl enable noip.service
systemctl start noip.service
systemctl status noip.service

