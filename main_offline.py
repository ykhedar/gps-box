#!/usr/bin/env python

# System Level Imports
import os
import datetime
import time
import yaml
import logging

# Module Imports
import ublox
import mcast

MAIN_LOG_DIR="/home/ankommen/Event/projects/GWR/record/aeroinspekt/"

CURRENT_DATE_TIME=datetime.datetime.now().isoformat().replace(":", "-")
INIT_LOG_DIR=MAIN_LOG_DIR+"logs/init/"
INIT_LOG_FILE=CURRENT_DATE_TIME+".log"

if not os.path.exists(os.path.dirname(INIT_LOG_DIR)):
		os.makedirs(os.path.dirname(INIT_LOG_DIR))

logging.basicConfig(filename=INIT_LOG_DIR+INIT_LOG_FILE, filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
logging.info("Starting Ublox Python script.")

logging.info("Looping until tun0 is up.")
while True:
	iface_str = os.popen('ip addr show tun0').read()
	if iface_str!='':
		if iface_str.find('10.8.0.')!=-1:
			logging.info("VPN is active. IP Address acquired.")
			break
	logging.info("VPN is not active yet. Waiting 5 more seconds.")
	time.sleep(5)

ip_string = iface_str.split("inet ")[1].split(" ")[0]
MY_IP = ip_string.split('/')[0]
logging.info("My IP Address from VPN is: " + MY_IP)

multicast_sender = mcast.MultiCastSender(MY_IP)
logging.info("Multicast Sender Initialised")

dev = ublox.UBlox("/home/ankommen/Desktop/2019-06-15T03-02-08.914126.ubx")
dev2 = ublox.UBlox("/home/ankommen/Desktop/2019-06-15T03-02-14.636405.ubx")

BOX_POS_LOG_DIR=MAIN_LOG_DIR + "logs/boxes/" + "1_2" + "/"
if not os.path.exists(os.path.dirname(BOX_POS_LOG_DIR)):
		os.makedirs(os.path.dirname(BOX_POS_LOG_DIR))

pos_log_file=open(BOX_POS_LOG_DIR+CURRENT_DATE_TIME+".log", "wa",buffering=1)
pos_log_file2=open(BOX_POS_LOG_DIR+CURRENT_DATE_TIME+"_2.log", "wa",buffering=1)

logging.info("Starting Data acquisition loop from UBLOX. ")
while True:
	msg = dev.receive_message(ignore_eof=True)
	msg2 = dev2.receive_message(ignore_eof=True)
	if msg is None:
		logging.info("No Message from device 1.")
		break
	if msg2 is None:
		logging.info("No Message from device 2.")
		break

	if msg.name() == "NAV_POSLLH":
		msg.unpack()
		location=19
		if hasattr(msg, 'iTOW'):
			string_payload = str(2058)+","+ str(msg.iTOW) + "," +"1" + "," + "07k"+ "," + str(msg.Longitude) + "," + str(msg.Latitude) + "," + "0"+ "," + str(location) + "\n"
			multicast_sender.send_data(string_payload)
			pos_log_file.write(string_payload)

	if msg2.name() == "NAV_POSLLH":
		msg2.unpack()
		location=19
		if hasattr(msg2, 'iTOW'):
			# Box2 Data 
			string_payload2 = str(2058)+","+ str(msg2.iTOW) + "," +"2" + "," + "07g"+ "," + str(msg2.Longitude) + "," + str(msg2.Latitude) + "," + "0"+ "," + str(location) + "\n"
			multicast_sender.send_data(string_payload2)
			pos_log_file2.write(string_payload2)

	time.sleep(0.1)
pos_log_file.close()
pos_log_file2.close()

