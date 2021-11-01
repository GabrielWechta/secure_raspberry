import pyshark
from itertools import cycle
import matplotlib.pyplot as plt
import scipy.stats
import pandas as pd
import numpy as np


def start_live_capture(how_many_packets_sniff: int, dict_key_name: str, list_of_dict: list = None) \
        -> list:
    capture = pyshark.LiveCapture(interface='wlp4s0',
                                  bpf_filter="tcp src port 80 or tcp dst port 80")
    capture.sniff(packet_count=how_many_packets_sniff)
    print(capture)

    if list_of_dict is None:
        list_of_dict = []
        for packet in capture:
            if str(packet['tcp'].flags) == "0x00000012":  # SYN/ACK flag
                time_relative_float = float(packet['tcp'].time_relative)
                dictionary_data = {dict_key_name: time_relative_float}
                list_of_dict.append(dictionary_data)
    else:
        for packet, time_dict in zip(capture, list_of_dict):
            if str(packet['tcp'].flags) == "0x00000012":  # SYN/ACK flag
                time_relative_float = float(packet['tcp'].time_relative)
                time_dict[dict_key_name] = time_relative_float

    return list_of_dict


def merge_two_list_of_dict(list_od_dict_1: list, list_of_dict_2: list) -> list:
    list_of_dict_full = []
    # zipped_list = zip(list_od_dict_1, cycle(list_of_dict_2)) if len(list_od_dict_1) > len(
    #     list_of_dict_2) else zip(cycle(list_od_dict_1), list_of_dict_2)
    for i, (dict_1, dict_2) in enumerate(zip(list_od_dict_1, list_of_dict_2)):
        dict_full = {"index": i, **dict_1, **dict_2, }
        list_of_dict_full.append(dict_full)
    return list_of_dict_full


def merge_two_list_of_dict_2(list_od_dict_1: list, list_of_dict_2: list) -> list:
    list_of_dict_full = []
    # zipped_list = zip(list_od_dict_1, cycle(list_of_dict_2)) if len(list_od_dict_1) > len(
    #     list_of_dict_2) else zip(cycle(list_od_dict_1), list_of_dict_2)
    for dict_1, dict_2 in zip(list_od_dict_1, list_of_dict_2):
        dict_full = {"time": dict_1["beta_1"], "type": "beta_1"}
        list_of_dict_full.append(dict_full)
        dict_full = {"time": dict_2["beta_2"], "type": "beta_2"}
        list_of_dict_full.append(dict_full)
    return list_of_dict_full


def filter_outliers(data_frame: pd.DataFrame) -> pd.DataFrame:
    z_scores = scipy.stats.zscore(data_frame)
    abs_z_scores = np.abs(z_scores)
    filtered_entries = (abs_z_scores < 2).all(axis=1)
    return data_frame[filtered_entries]


if __name__ == "__main__":
    list_of_dict_beta_1 = start_live_capture(100 * 3, "beta_1")

    list_of_dict_beta_2 = start_live_capture(100 * 3, "beta_2")
    list_of_dict_two_betas = merge_two_list_of_dict(list_of_dict_beta_1, list_of_dict_beta_2)
    df = pd.DataFrame(list_of_dict_two_betas)
    df = filter_outliers(df)

    ax1 = df.plot(kind='scatter', x='index', y='beta_1', color='r', label="beta_1")
    ax2 = df.plot(kind='scatter', x='index', y='beta_2', color='b', label="beta_2", ax=ax1)
    print(df.mean(axis=0))
    print(df.median(axis=0))

    plt.show()

    # plt.show()
