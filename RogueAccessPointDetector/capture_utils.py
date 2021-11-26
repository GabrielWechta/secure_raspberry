import numpy as np
import pandas as pd
import pyshark
import scipy.stats

from network_manager_utils import get_wireless_network_interface


def start_live_capture(packets_number: int, dict_key_name: str,
                       wireless_network_interface: str = None,
                       relative_time_per_ap_list: list = None) -> list:
    if wireless_network_interface is None:
        wireless_network_interface = get_wireless_network_interface()

    capture = pyshark.LiveCapture(interface=wireless_network_interface,
                                  bpf_filter="tcp src port 80 or tcp dst port 80")

    # We need to receive SYN, SYN/ACK, ACK packets, so it requires 3 frame per packet
    capture.sniff(packet_count=packets_number * 3)

    # print(capture)

    if relative_time_per_ap_list is None:
        relative_time_per_ap_list = []  # creating empty list for dictionary of time entries
        for packet in capture:
            if str(packet['tcp'].flags) == "0x00000012":  # SYN/ACK flag
                time_relative_float = float(packet['tcp'].time_relative)  # getting relative time
                dictionary_data = {dict_key_name: time_relative_float}
                relative_time_per_ap_list.append(dictionary_data)
    else:
        for packet, time_dict in zip(capture, relative_time_per_ap_list):
            if str(packet['tcp'].flags) == "0x00000012":  # SYN/ACK flag
                time_relative_float = float(packet['tcp'].time_relative)
                time_dict[dict_key_name] = time_relative_float

    return relative_time_per_ap_list


def merge_two_lists_of_dict(list_of_dict_1: list, list_of_dict_2: list) -> list:
    list_of_dict_full = []
    for i, (dict_1, dict_2) in enumerate(zip(list_of_dict_1, list_of_dict_2)):
        dict_full = {"index": i, **dict_1, **dict_2}
        list_of_dict_full.append(dict_full)
    return list_of_dict_full


def filter_outliers(data_frame: pd.DataFrame) -> pd.DataFrame:
    z_scores = scipy.stats.zscore(data_frame)
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 3).all(axis=1)
    return data_frame[filtered_entries]
