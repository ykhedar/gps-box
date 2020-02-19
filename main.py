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

MAIN_LOG_DIR="/home/debian/Event/projects/GWR/record/aeroinspekt/"

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

configs = yaml.load(open('config.yaml', 'r'))
BOX_ID = MY_IP.split(".")[-1][0]
KEY = 'BOX'+str(BOX_ID)
OFFSET = configs[KEY]['OFFSET']
KRANID = configs[KEY]['KRANID']
logging.info("Box Id as read from config.yaml file and my IP is: "+str(BOX_ID))

# Create ublox Log directory and log file based on current time.
UBX_RAW_LOG_DIR = MAIN_LOG_DIR + "logs/ublox/"
if not os.path.exists(os.path.dirname(UBX_RAW_LOG_DIR)):
		os.makedirs(os.path.dirname(UBX_RAW_LOG_DIR))

UBX_RAW_LOG_FILE = UBX_RAW_LOG_DIR + CURRENT_DATE_TIME + ".ubx"
logging.info("Logging ublox RAW data to the file: " + str(UBX_RAW_LOG_FILE))
dev = ublox.UBlox("/dev/ttyS1")
dev.set_logfile(UBX_RAW_LOG_FILE)

BOX_POS_LOG_DIR=MAIN_LOG_DIR + "logs/boxes/" + str(BOX_ID) + "/"
if not os.path.exists(os.path.dirname(BOX_POS_LOG_DIR)):
		os.makedirs(os.path.dirname(BOX_POS_LOG_DIR))

BOX_POS_LOG_FILE=BOX_POS_LOG_DIR+CURRENT_DATE_TIME+".log"

pos_log_file=open(BOX_POS_LOG_FILE, "wa",buffering=1)
logging.info("Logging Processed data to the file: " + str(BOX_POS_LOG_FILE))
logging.info("Starting Data acquisition loop from UBLOX. ")
GPS_WEEK="null"
rtk_status = 0
while True:
	msg = dev.receive_message(ignore_eof=True)
	if msg is None:
		logging.info("No Message.")
		break
	if msg.name() == "NAV_TIMEGPS":
		msg.unpack()
		GPS_WEEK=str(msg.week)
	if msg.name() == "NAV_STATUS":
		msg.unpack()
		rtk_status = bin(msg.flags)[8]
	if msg.name() == "NAV_POSLLH":
		msg.unpack()
		location=19
		if hasattr(msg, 'iTOW'):
			string_payload = GPS_WEEK+","+ str(msg.iTOW) + "," +str(BOX_ID) + "," + str(KRANID)+ "," + \
							 str(msg.Longitude) + "," + str(msg.Latitude) + "," + str(OFFSET) + "," + str(msg.hAcc) + "," + \
			str(rtk_status)
			# GPS-week, GPS-TimeOfWeek,BOX-ID,Crane-ID,LONGITUDE, LATITUDE, OFFSET, hAcc, RTK-Status, HASH
			msg_to_send = string_payload + "," + str(len(string_payload))
			multicast_sender.send_data(msg_to_send)
			msg_to_write = msg_to_send + "\n"
			pos_log_file.write(msg_to_write)

pos_log_file.close()

