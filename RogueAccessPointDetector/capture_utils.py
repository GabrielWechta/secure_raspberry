import numpy as np
import pandas as pd
import pyshark
import scipy.stats
from matplotlib import pyplot as plt

from network_manager_utils import get_wireless_network_interface


def start_live_capture(packets_number: int,
                       dict_key_name: str,
                       wireless_network_interface: str = None):
    if wireless_network_interface is None:
        wireless_network_interface = get_wireless_network_interface()
    print("hej")

    capture = pyshark.LiveCapture(interface=wireless_network_interface,
                                  bpf_filter="host 212.82.100.150 and tcp port 80")

    capture.sniff(packet_count=packets_number * 3)

    list_of_dict_relative_time = []
    for packet in capture:
        # print(packet)
        if str(packet['tcp'].flags) == "0x00000012":  # SYN/ACK flag
            time_relative_float = float(packet['tcp'].time_relative)  # getting relative time
            dictionary_data = {dict_key_name: time_relative_float}
            list_of_dict_relative_time.append(dictionary_data)

    return list_of_dict_relative_time


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


if __name__ == "__main__":
    list_of_dict_beta_1 = start_live_capture(100, "beta_1")

    list_of_dict_beta_2 = start_live_capture(100, "beta_2")
    list_of_dict_two_betas = merge_two_lists_of_dict(list_of_dict_beta_1, list_of_dict_beta_2)
    df = pd.DataFrame(list_of_dict_two_betas)
    df = filter_outliers(df)

    ax1 = df.plot(kind='scatter', x='index', y='beta_1', color='r', label="beta_1")
    ax2 = df.plot(kind='scatter', x='index', y='beta_2', color='b', label="beta_2", ax=ax1)
    print(df.mean(axis=0))
    print(df.median(axis=0))

    plt.show()
