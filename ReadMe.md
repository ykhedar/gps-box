# gps-box

This repository contains the scripts used to run 
on the GPS Boxes of Project AeroInspekt.

There are three main scripts:
1. init.sh: This is the main script and is run using a service aeroinspekt.service
2. main.py: This starts the ublox Decoder(based on ublox.py from https://github.com/tridge/pyUblox)
   and a multicast sender for transmitting the useful information on a multicast group. The 
   file config.yaml contains the ip addresses of all involved clients
3. mcast.py: This is the class for multicast sender used in main.py 
   
# Dependencies
python-yaml
python-serial


# Howto 
For first installation:  
1. Copy the ankommen.service to /etc/systemd/system/ folder

```bash
sudo cp /home/debian/gps-box/aeroinspekt.service /etc/systemd/system/aeroinspekt.service
```

2. Now enable the service

```bash
sudo systemctl enable aeroinspekt.service
```

3. Start the service
```bash
sudo systemctl start aeroinspekt.service
```

4. Check if the service is running
```bash
sudo systemctl status aeroinspekt.service
```

Now from next boot onwards the service will be on during boot automatically.



# Don't
- Don't remove the Event, gps-box folders and the *.ovpn file found in the /home/debian of the boxes


# Important points:
- The VPN Client configures the traffic routing during initialisation and hence it is
important that the internet providing device is up and running before the openvpn is 
started. 
The corresponding output is as follows: 

ROUTE_GATEWAY 192.168.1.1/255.255.255.0 IFACE=eth0 HWADDR=xx:xx:xx:xx:xx

In this case the computer is connected to a local router.
 A sample log can be found in the logs/ directory of this repository.
 
 The log can be viewed with the following command
 
 ```bash
 journalctl -u aeroinspekt.service
 ```
 
- When OpenVPN starts it sets a qlen=100. It might be interesting to see the effects of
this on the openvpn speed.

- 

## Crontab for restarting the boxes every 20 minutes.

```bash
sudo crontab -e
```
Put this crontab with sudo.
```bash
*/20 * * * * /sbin/shutdown -r now
```


# Logging.
Logs are stored at /home/debian/Event/projects/GWR/record because, the memory card is mounted at this location