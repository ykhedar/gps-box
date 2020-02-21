#!/usr/bin/env bash

# disable onboard heartbeat LED
echo none > /sys/class/leds/beaglebone:green:usr0/trigger

# Check if the internet access is available. If yes start the openvpn.
# This is needed to ensure the vpn routes the traffic through the internet
# providing interface.

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
sleep 5


# Start the Internet Network Monitor
cd /home/debian/gps-box && python internet_check.py &
sleep 5

# Start the git repo status script
cd /home/debian/gps-box && python git_check.py &
sleep 15

cd /home/debian && sh start_str2str.sh &
