#!/bin/bash
# Run with root privileges.

# Repositories
apt-get update
apt-get upgrade -y

# Sniffer 
apt-get install tcpflow -y

# ncat - Netcat for XXI century
apt install ncat -y

# Docker
apt install -y docker.io
sudo systemctl enable docker --now
sudo usermod -aG docker $USER

# Repositories again
apt-get update
apt-get upgrade -y
apt-get autoremove -y