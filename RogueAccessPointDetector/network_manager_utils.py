import subprocess
import re

import netifaces
import nmcli
from itertools import chain


def show_wifi_devices() -> None:
    """
    Display available Access Points.
    """
    for dev in nmcli.device.wifi():
        print(dev)


def build_wifi_devices_dictionary() -> dict:
    """
    Build dictionary of available wifi devices.

    :return: dictionary of available wifi devices following pattern [key = BSSID, value = SSID].
    """
    wifi_dev_dict = {}
    for dev in nmcli.device.wifi():
        wifi_dev_dict[dev.bssid] = dev.ssid

    # TODO during testing I discovered that in my neighbourhood there are four AP with the same
    #  SSID (sic!). In order to keep script in normal behaviour, I delete this entry by hand.
    wifi_dev_dict.pop('34:2C:C4:C6:AA:DC', None)
    wifi_dev_dict.pop('AE:22:15:AB:3E:D8', None)
    wifi_dev_dict.pop('3A:43:1D:C3:C9:EA', None)

    return wifi_dev_dict


def look_for_repeated_ssid(bssid_ssid_dict: dict):
    """
    Find first two BSSID for APs with same SSID.

    :param bssid_ssid_dict: dictionary of available wifi devices following pattern [key = BSSID, value = SSID]
    :return: Two BSSIDs with same SSID.
    """
    reverse_multi_dict = {}
    for key, value in bssid_ssid_dict.items():
        reverse_multi_dict.setdefault(value, set()).add(key)

    repeated_sets = [values for key, values in reverse_multi_dict.items() if len(values) > 1]

    bssid_of_repeated_sets = list(chain.from_iterable(repeated_sets))

    return bssid_of_repeated_sets[0], bssid_of_repeated_sets[1]


def connect_to_network_by_bssid(bssid: str) -> bool:
    """
    Call to connect to wifi network with given BSSID. This is extra wrapper for nmcli (Network
    Manager Command Line Interface), that does not come with python library nmcli. Because of the
    necessity to inject string to shell command, this function should be used with caution.
    Before executing shell command, regular expression is used to check whether function's input
    follows WPA BSSID pattern.

    :param bssid: Wireless network's Basic Service Set Identifier.
    :return: True if connection was established, device is connected to wireless network. False if
    there was an error during connection or input did not follow WPA BSSID pattern.
    """
    bssid_pattern = re.compile(r"([0-9A-F]{2}([:-]|$)){6}")
    if bssid_pattern.match(bssid):
        nmcli_command = f"nmcli device wifi connect {bssid}"
        try:
            subprocess.check_call(nmcli_command, shell=True)
            return True
        except subprocess.CalledProcessError:
            print(f"Error during connecting by {nmcli_command}.")
    else:
        print("Input given to this function does not follow WPA BSSID pattern.")

    return False


def get_wireless_network_interface() -> str:
    """
    Get some available wireless network interface card. This function assumes that wireless
    interface begins with 'w'.

    :return: Name of some available wireless network interface card.
    """
    network_interfaces_cards = netifaces.interfaces()
    for nic in network_interfaces_cards:
        if nic.startswith("w"):
            return nic

    raise ValueError("No wireless network interface card has been found.")
