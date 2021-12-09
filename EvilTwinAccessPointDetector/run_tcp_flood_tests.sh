#!/bin/bash
for i in {1..5}; do
  nmcli device wifi connect 6C:60:EB:87:88:99
  sudo python3 tcp_flood.py --target_bssid 6C:60:EB:87:88:99 --destination_ip 172.217.16.35 --destination_port 80 --packets_number 100

  sleep 2

  nmcli device wifi connect 64:66:B3:1E:26:EF
  sudo python3 tcp_flood.py --target_bssid 64:66:B3:1E:26:EF --destination_ip 172.217.16.35 --destination_port 80 --packets_number 100
done
