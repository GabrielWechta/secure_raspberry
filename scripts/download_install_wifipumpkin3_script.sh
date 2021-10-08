#!bin/bash
# Run with root privileges.

apt install python3-pyqt5 hostapd -y
apt install libssl-dev libffi-dev build-essential -y
git clone https://github.com/P0cL4bs/wifipumpkin3
cd wifipumpkin3
python3 setup.py install

wifipumpkin3

# for more details how to set up RAP: https://www.kalilinux.in/2020/12/wifi-pumpkin-3-dengerous-access-point.html