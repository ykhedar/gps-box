# gps-box
## Installing Debian on Beaglebone Black.
### Follow the instructions here:
https://beagleboard.org/getting-started
https://www.youtube.com/watch?v=oRGrm8RfGCE

Basically:
1. Download the file bone-eMMC-flasher-debian-9.11-console-armhf-2019-12-01-1gb.img.xz from
https://elinux.org/Beagleboard:BeagleBoneBlack_Debian#Flashing_eMMC
or a newer version. But note the 'eMMC-flasher' in the name. This is important
2. Format the SD Card
3. Flash the SD Card using BalenaEtcher (you dont have to decompress the image.)
4. Insert the SD card into the BBB. Hold down the User/Boot button as shown in the tutorials, and power up 
   either using the Barrel connector or a Mini USB cable. Release the button when all LEDs are steady.
5. Wait unti the Flashing is done. Could be 4-5minutes. The LEDs would be steady and then go off. 
6. Remove Power and Remove the SD Card.
7. Now connect using the Mini USB cable to a computer for setting up. Done.

 
This repository contains the scripts used to run 
on the GPS Boxes of Project AeroInspekt.

There are three main scripts:
1. init.sh: This is the main script and is run using a service aeroinspekt.service
2. main.py: This starts the ublox Decoder(based on ublox.py from https://github.com/tridge/pyUblox)
   and a multicast sender for transmitting the useful information on a multicast group. The 
   file config.yaml contains the ip addresses of all involved clients
3. mcast.py: This is the class for multicast sender used in main.py 
   
# Dependencies
1. Install Some dependencies and clone the git repository.
```bash
sudo apt update && sudo apt install -y git python-yaml python-serial openvpn usbutils usb-modeswitch libusb-1.0 build-essential && sudo apt upgrade sudo apt upgrade bb-cape-overlays && rm -rf /var/lib/apt/lists/*

cd ~ && git clone https://github.com/ykhedar/gps-box.git && git clone https://github.com/rtklibexplorer/RTKLIB.git
cd ~/RTKLIB/app/str2str/gcc/ && make && sudo make install && rm -rf ~/RTKLIB
```

2. Copy the *.ovpn file in the home directory to enable the ovpn. From the folder boxes_copy

```bash
scp box[123456].ovpn debian@10.8.0.[123456]1:/home/debian/box[123456].ovpn
scp start_str2str.sh debian@10.8.0.[123456]1:/home/debian/start_str2str.sh
```

3. Copy the ankommen.service to /etc/systemd/system/ folder. Now enable the service. Then Either Restart the system or
   Run start it manually for the first time to check if it works.
```bash
sudo cp /home/debian/gps-box/aeroinspekt.service /etc/systemd/system/aeroinspekt.service
sudo systemctl enable aeroinspekt.service
```

4. Check if the service is running
```bash
sudo systemctl status aeroinspekt.service
```

5. Add the user into sudoers list to execute the shutdown command.

```bash
sudo visudo
```

Add the following line at the end of the file.

```bash
debian ALL=/sbin/shutdown
debian ALL=NOPASSWD: /sbin/shutdown
```


# Don't
- Don't remove the Event, gps-box folders and the *.ovpn file found in the /home/debian of the boxes


# Important points:
- The VPN Client configures the traffic routing during initialisation and hence it is
important that the internet providing device is up and running before the openvpn is 
started. 
The corresponding output is as follows: 

ROUTE_GATEWAY 192.168.1.1/255.255.255.0 IFACE=eth0 HWADDR=xx:xx:xx:xx:xx

In this case the computer is connected to a local router.

## Viewing the Service Logs

A sample log can be found in the logs/ directory of this repository.
The log can be viewed with the following command
 
 ```bash
 journalctl -u aeroinspekt.service
 ```
 
- When OpenVPN starts it sets a qlen=100. It might be interesting to see the effects of
this on the openvpn speed.

## To make the RTC work
This will update the overlay with RTC-D3231 which we are using for our project. Next one needs to 
activate the overlay so that it will load during the boot before anything else and the RTC can be read by 
the hwclock.

Now update the /boot/uEnv.txt

```bash
uboot_overlay_addr4=/lib/firmware/BB-I2C2-RTC-DS3231.dtbo
uboot_overlay_addr5=/lib/firmware/BB-UART1-00A0.dtbo
uboot_overlay_addr6=/lib/firmware/BB-UART2-00A0.dtbo

cape_enable=capemgr.enable_partno=BB-UART1,BB-UART2
```

## Crontab for restarting the boxes every 24 hours.

```bash
sudo crontab -e
```
Put this crontab with sudo. This reboots the board every day at 03:00 hrs
```bash
* 3 * * * /sbin/shutdown -r now
```


# Logging.
Logs are stored at /home/debian/Event/projects/GWR/record because, the memory card is mounted at this location
