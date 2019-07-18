#!/usr/bin/env python

import os
import time
import datetime

MAIN_LOG_DIR="/home/debian/Event/projects/GWR/record/aeroinspekt/"
CURRENT_DATE_TIME=datetime.datetime.now().isoformat().replace(":", "-")
GIT_LOG_DIR=MAIN_LOG_DIR+"logs/internet/"
GIT_LOG_FILE=GIT_LOG_DIR+CURRENT_DATE_TIME+".log"


if not os.path.exists(os.path.dirname(GIT_LOG_DIR)):
		os.makedirs(os.path.dirname(GIT_LOG_DIR))

log_file = open(GIT_LOG_FILE, "wa", buffering=1)

while True:
	os.popen('')
	git_status=os.popen('cd /home/debian/gps-box/ && git remote show origin').read()

	if "local out of date" in git_status:
		pull_result=os.popen('cd ~ && rm -rf gps-box/ && git clone https://github.com/ykhedar/gps-box.git').read()
		log_file.write(datetime.datetime.now().isoformat() + "," + pull_result + "\n")
		log_file.write(datetime.datetime.now().isoformat() + ", doing a system restart to make changes in git take effect." + "\n")
		shutdow_result=os.popen("shutdown -r now").read()
		log_file.write(datetime.datetime.now().isoformat() + "," +shutdow_result+ "\n")

	else:
		log_file.write(datetime.datetime.now().isoformat() + ", git is already updated. Waiting for 1 minutes" + "\n")
	time.sleep(60)

log_file.close()