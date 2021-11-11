#!/bin/bash
# Run with root privileges.

# Repositories
apt-get update
apt-get upgrade -y

# CLI utils
apt install tree -y
apt-get install tshark -y

# Sniffer 
apt-get install tcpflow -y

# ncat - Netcat for XXI century
apt install ncat -y

# Docker
apt install -y docker.io
sudo systemctl enable docker --now
sudo usermod -aG docker $USER

# xterm for capture_WPA.sh
apt-get install xterm -y

# Hashcat tools
apt-get install libcurl4-openssl-dev libssl-dev pkg-config

cd ~/opt
git clone https://github.com/ZerBea/hcxdumptool.git
cd hcxdumptool
make
make install

cd ~/opt
git clone https://github.com/ZerBea/hcxtools.git
cd hcxtools
make
make install

cd ~/opt
git clone https://github.com/hashcat/hashcat.git
cd hashcat
make 
make install

# Repositories again
apt-get update
apt-get upgrade -y
apt-get autoremove -y