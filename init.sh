#!/usr/bin/env bash

# disable onboard heartbeat LED
echo none > /sys/class/leds/beaglebone:green:usr0/trigger

# start the Event software. At the moment this needs to be done for the
# python script to work.
#/home/debian/Event/bin/Event /home/debian/Event/projects/GWR -i  -v &

# wait for some time for the Event to work out, VPN and the LTE to connect properly.
#sleep 60

# kill Event to free the Ublox Port
#killall Event

# Check if the internet is there. If yes start the openvpn
until $(ping -q -c 1 -W 1 8.8.8.8 >/dev/null); do
    printf 'No internet. Waiting for 5 seconds\n\n'
    sleep 5
done

# Start the openvpn
printf 'We have internet now. Try to start OpenVPN\n\n'
openvpn /home/debian/*.ovpn &

sleep 15

# Start the python Ublox Receiver
cd /home/debian/gps-box && python main.py &

# Start the Internet Network Monitor
cd /home/debian/gps-box && python internet_check.py &

# Start the git repo status script
cd /home/debian/gps-box && python git_check.py &

sleep 15

cd /home/debian && sh start_str2str.sh &
