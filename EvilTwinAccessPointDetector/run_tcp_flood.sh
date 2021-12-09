#!/bin/bash
# Run with root privileges.
target_bssid=${target_bssid:-"not_specified"}
destination_ip=${destination_ip:-"not_specified"}
destination_port=${destination_port:-"not_specified"}
packets_number=${packets_number:-100}

while [ $# -gt 0 ]; do

  if [[ $1 == *"--"* ]]; then
    param="${1/--/}"
    declare "$param"="$2"
  fi

  shift
done
echo $target_bssid
nmcli device wifi connect "$target_bssid"

sleep 1

sudo python3 tcp_flood.py --target_bssid "$target_bssid" --destination_ip "$destination_ip" \
--destination_port "$destination_port" --packets_number "$packets_number"


