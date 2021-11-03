#!bin/bash
# Run with root privileges.
ssid=${ssid:-NewFreeWiFi}
wnic_interface=${ap_interface:-wlan1}

while [ $# -gt 0 ]; do

  if [[ $1 == *"--"* ]]; then
    param="${1/--/}"
    declare "$param"="$2"
    echo "$1" "$2"
  fi

  shift
done

airmon-ng start {wnic_interface}