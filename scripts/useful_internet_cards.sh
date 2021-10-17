# Ways of getting your IP addresses
# Public:
# IPv4:
curl -4 icanhazip.com 
curl ifconfig.me
# IPv6
curl -6 icanhazip.com 
curl ident.me

# Private:
hostname -I | awk '{print $1}'

# Put your wireless card into monitor mode by typing 
airmon-ng start wlan1

# Write internet packets to a file
tcpdump -w somefile --print 
# or
tcpflow -i wlan1 -f

# In order to see all Wifi Networks nearby
nmcli dev wifi
# With even more details
nmcli -f ALL dev wifi

# In order to deauthenticate
aireplay-ng -00 -a [BSSID of AP] wlan0mon

# To find out all devices in internal network
hostname -I # for local address
nmap -sP $local_IP_with_zero_at_ethe_end/24

# To copy files over ssh
scp remote_username@10.10.0.2:/remote/file.txt /local/directory

# Mapping ports of given address
nmap --top-ports 20 $address

# An easy way to start TCP 3-way handhsake is simply
wget $address:80 # 80/tcp - http, 443/tcp - https

