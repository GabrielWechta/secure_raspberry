#!bin/bash
# Run with root privileges.

# apt-get install hostapd dnsmasq apache2 # required packages

airmon-ng start wlan1

echo "Configuration is being done."
echo "I am assuming default locations for config files."
if [ -e /root/fake_access_point ]; then
  echo "File /root/fake_access_point already exists!"
else
  mkdir /root/fake_access_point
fi

# cd /root/fake_access_point

# Creating hostapd.conf 
hostapd_config="interface=wlan1mon\ndriver=nl80211\nssid=New_Way_2\nhw_mode=g\nchannel=1\nmacaddr_acl=0\nignore_broadcast_ssid=0\n" 

echo -en $hostapd_config > /root/fake_access_point/hostapd.conf 

echo "Starting Host Access Point Deamon..."
xterm -title "hostapd" -e hostapd /root/fake_access_point/hostapd.conf &
sleep 1

# Creating dnsmasq.conf 
dnsmasq_config="interface=wlan1mon\ndhcp-range=192.168.1.2, 192.168.1.30, 255.255.255.0, 12h\ndhcp-option=3, 192.168.1.1\ndhcp-option=6, 192.168.1.1\nserver=8.8.8.8\nlog-queries\nlog-dhcp\nlisten-address=127.0.0.1\n"

echo -en $dnsmasq_config > /root/fake_access_point/dnsmasq.conf 

# Routing table and gateway
# Now we need to assign the interface a network gateway and netmask and then add the routing table.
ifconfig wlan1mon up 192.168.1.1 netmask 255.255.255.0
route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1

echo "Starting Domain Name System (DNS) and Dynamic Host Configuration Protocol (DHCP)..."
xterm -title "dnsmasq" -e dnsmasq -C /root/fake_access_point/dnsmasq.conf -d &
sleep 1

echo "Forwarding traffic from wlan0, to wlan1mon."
# Internet access 
iptables --table nat --append POSTROUTING --out-interface wlan0 -j MASQUERADE # Interface name that is used to forward traffic from.
iptables --append FORWARD --in-interface wlan1mon -j ACCEPT # Interface name to receive the packets or the interface that is being forwarded to.

echo "Enabling IP Forwarding..."
echo 1 > /proc/sys/net/ipv4/ip_forward

echo "Fake Access Point started."

# x-terminal-emulator -e bash test.sh 

