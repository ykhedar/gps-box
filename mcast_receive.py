#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.
import time
import struct
import socket
import sys

MYPORT = 4444
MYGROUP_4 = '225.0.0.37'  
group=MYGROUP_4


# Look up multicast group address in name server and find out IP version
addrinfo = socket.getaddrinfo(group, None)[0]

# Create a socket
s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

# Bind it to the port
s.bind(('0.0.0.0', MYPORT))

# Join group
mreq = socket.inet_aton(MYGROUP_4) + socket.inet_aton('10.8.0.6')
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Loop, printing any data we receive
print("Waiting to recieve.")
while True:
    data, sender = s.recvfrom(32)
    print("Sender: ", sender, "Data: ", data)
