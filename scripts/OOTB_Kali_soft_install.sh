#!/bin/bash
# Run with root privileges.

# Repositories
apt-get update
apt-get upgrade -y

# Package Menagers
apt-get install snapd -y
systemctl enable --now snapd apparmor

# Python
apt install python3-pip -y

# Java
apt install default-jre -y

# Web Browser - Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P /tmp
dpkg -i /tmp/google-chrome-stable_current_amd64.deb

# VCS 
apt-get install git -y

# Gedit
apt-get install gedit -y

# VS Code
apt install curl gpg software-properties-common apt-transport-https 
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" | tee /etc/apt/sources.list.d/vscode.list
apt update
apt install code -y

# Notepad++
snap install notepad-plus-plus

# Markdown editor - ReText
apt-get install retext -y

# Mendeley Desktop
apt-get install mendeleydesktop -y

# Media Player - VLC 
sudo snap install vlc

# Repositories again
apt-get update
apt-get upgrade -y
apt-get autoremove -y