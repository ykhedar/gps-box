#!/usr/bin/env python

import os
import datetime
import time

MAIN_LOG_DIR="/home/debian/"
CURRENT_DATE_TIME=datetime.datetime.now().isoformat().replace(":", "-")
NET_LOG_DIR=MAIN_LOG_DIR+"logs/internet/"
NET_LOG_FILE=NET_LOG_DIR+CURRENT_DATE_TIME+".log"


if not os.path.exists(os.path.dirname(NET_LOG_DIR)):
		os.makedirs(os.path.dirname(NET_LOG_DIR))

log_file = open(NET_LOG_FILE, "wa", buffering=1)
internet_status = False
vpn_status = False

while True:
	internet_ping = os.popen('ping -c 1 -w 1 8.8.8.8').read().split('\n')
	vpn_ping = os.popen('ping -c 1 -w 1 10.8.0.1').read().split('\n')

	if len(internet_ping) > 1:
		internet_status = str(bool(internet_ping[1]))
	else:
		internet_status = str(bool(False))

	if len(vpn_ping) > 1:
		vpn_status = str(bool(vpn_ping[1]))
	else:
		vpn_status = str(bool(False))
	log_file.write(datetime.datetime.now().isoformat() + "," + internet_status + "," + vpn_status + "\n")
	time.sleep(5)

log_file.close()
