#!bin/bash

# Put your wireless card into monitor mode by typing 
airmon-ng start wlan1

# Write packets to a file
tcpdump -w somefile --print 
# or
tcpflow -i wlan1 -f

# in order to see all Wifi Networks nearby
nmcli dev wifi
#with even more detail
nmcli -f ALL dev wifi

# In order to deauthenticate
aireplay-ng -00 -a [BSSID of AP] wlan0mon

