import numpy as np
import pandas as pd
import pyshark
import scipy.stats

from network_manager_utils import get_wireless_network_interface


def start_live_capture(packets_number: int,
                       dict_key_name: str,
                       destination_ip: str,
                       destination_port: int,
                       wireless_network_interface: str = None) -> list:
    """
    Start capturing packets from **wireless_network_interface** interface.

    Capture will listen for **packets_number** packets, than it will make list of dictionaries
    where key is the **dict_key_name** and value is relative time of receiving SYN/ACK from the
    time os sending SYN.


    :param packets_number: How many packets will pyshark.LiveCapture sniff.
    :param dict_key_name: Name of the AP for the relative time dictionary.
    :param destination_ip: Under test remote server's IP.
    :param destination_port: Under test remote server's open port. Typically 80.
    :param wireless_network_interface: Wireless Network Interface on which sniffing will be
    conducted.
    :return: List of dictionaries containing relative time from SYN to SYN/ACK for given AP.
    List of dictionaries is fastest way of creating pandas *DataFrame*.
    """

    if wireless_network_interface is None:
        wireless_network_interface = get_wireless_network_interface()

    capture = pyshark.LiveCapture(interface=wireless_network_interface,
                                  bpf_filter=f"host {destination_ip} and tcp port {destination_port}")

    """ In order to get SYN/ACK relative time ee need to capture SYN. GIven that bpf_filter must 
    look as above. Because of that we need to capture 3 times """
    capture.sniff(packet_count=packets_number * 3)

    list_of_dict_relative_time = []
    for packet in capture:
        if str(packet['tcp'].flags) == "0x00000012":  # SYN/ACK flag
            time_relative_float = float(packet['tcp'].time_relative)  # getting relative time
            dictionary_data = {dict_key_name: time_relative_float}
            list_of_dict_relative_time.append(dictionary_data)

    return list_of_dict_relative_time


def merge_two_lists_of_dict(list_of_dict_1: list, list_of_dict_2: list) -> list:
    """
    Merge two lists of dictionaries into one list.

    This function is used for making the best insert data type for pandas *DataFrame*.

    :param list_of_dict_1: List of dictionaries.
    :param list_of_dict_2: List of dictionaries.
    :return: Merged list of dictionaries.
    """
    list_of_dict_full = []
    for i, (dict_1, dict_2) in enumerate(zip(list_of_dict_1, list_of_dict_2)):
        dict_full = {"index": i, **dict_1, **dict_2}
        list_of_dict_full.append(dict_full)
    return list_of_dict_full


def filter_outliers(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Use z-score to remove outliers form data.

    :param data_frame: Pandas DataFrame with relative SYN/ACK times.
    :return: Pandas DataFrame with removed outliers.
    """
    z_scores = scipy.stats.zscore(data_frame)
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3).all(axis=1)
    return data_frame[filtered_entries]
