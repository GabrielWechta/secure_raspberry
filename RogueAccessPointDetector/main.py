"""
This code is implementation of Evil Twin Detection Algorithm from Gabriel Wechta's
Engineer Thesis.
"""
import argparse
import multiprocessing
import subprocess

import pandas as pd

from capture_utils import start_live_capture, merge_two_lists_of_dict, filter_outliers
from network_manager_utils import build_wifi_devices_dictionary, look_for_repeated_ssid


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evil Twin Access Point detector. This program uses TCP forwarding delay "
                    "phenomena to recognise Evil Twin from tru Access Point. Some variables may "
                    "be set by user (server's IP address, server's port), some are set by us ("
                    "number of packets)."
    )

    parser.add_argument(
        "--destination_ip",
        dest="destination_ip",
        type=str,
        help="IP address of tested server.",
    )

    parser.add_argument(
        "--destination_port",
        dest="destination_port",
        type=int,
        help="Open port of tested server.",
    )

    return parser.parse_args()


def run_tcp_flood(target_bssid, dest_ip, dest_port):
    subprocess.call(f"./run_tcp_flood.sh "
                    f"--target_bssid {target_bssid} "
                    f"--destination_ip {dest_ip} "
                    f"--destination_port {dest_port}",
                    shell=True)


if __name__ == "__main__":
    args = _parse_args()
    destination_ip = args.destination_ip
    destination_port = args.destination_port

    wifi_dev_dict = build_wifi_devices_dictionary()
    beta_1_bssid, beta_2_bssid = look_for_repeated_ssid(wifi_dev_dict)

    beta_1_flood_process = multiprocessing.Process(target=run_tcp_flood, args=(beta_1_bssid,
                                                                               destination_ip,
                                                                               destination_port))
    beta_1_flood_process.start()

    print("Starting capture for beta_1.")
    list_of_dict_time_beta_1 = start_live_capture(packets_number=100,
                                                  dict_key_name=f"beta_1",
                                                  destination_ip=destination_ip,
                                                  destination_port=destination_port)

    beta_1_flood_process.join()
    print("Finished capture for beta_1.")

    beta_2_flood_process = multiprocessing.Process(target=run_tcp_flood, args=(beta_2_bssid,
                                                                               destination_ip,
                                                                               destination_port))
    beta_2_flood_process.start()

    print("Starting capture for beta_2.")
    list_of_dict_time_beta_2 = start_live_capture(packets_number=100,
                                                  dict_key_name=f"beta_2",
                                                  destination_ip=destination_ip,
                                                  destination_port=destination_port)
    beta_2_flood_process.join()
    print("Finished capture for beta_2.")

    # Merging data from both AP.
    list_of_dict_time_merged = merge_two_lists_of_dict(list_of_dict_time_beta_1,
                                                       list_of_dict_time_beta_2)

    # Creating Dataframe with merged times for both APs.
    df = pd.DataFrame(list_of_dict_time_merged)

    # In order to remove noised data, we filter outliers.
    df = filter_outliers(df)

    means = df[["beta_1", "beta_2"]].mean(axis=0).values
    medians = df[["beta_1", "beta_2"]].median(axis=0).values
    beta_1_mean, beta_2_mean = means[0], means[1]
    beta_1_median, beta_2_median = medians[0], medians[1]

    if beta_1_mean >= beta_2_mean:
        legal_bssid = beta_1_bssid
    else:
        legal_bssid = beta_2_bssid

    print(f"Based on the mean value, legal AP has BSSID: {legal_bssid}.")
