import argparse
import time

import pandas as pd
from matplotlib import pyplot as plt

from network_manager_utils import get_wireless_network_interface
from capture_utils import start_live_capture, merge_two_lists_of_dict, filter_outliers


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This program executes tests for EvilTwinDetector."
    )

    parser.add_argument(
        "--real_ap_bssid",
        dest="real_ap_bssid",
        type=str,
        help="BSSID for true/valid Access Point.",
    )

    parser.add_argument(
        "--fake_ap_bssid",
        dest="fake_ap_bssid",
        type=str,
        help="BSSID for fake/ET Access Point.",
    )

    parser.add_argument(
        "--packets_number",
        dest="packets_number",
        type=int,
        help="Number of packets that will be sent during one test round.",
    )

    parser.add_argument(
        "--test_rounds_number",
        dest="test_rounds_number",
        type=int,
        help="Number of test rounds that will be conducted.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    real_ap_bssid = args.real_ap_bssid
    fake_ap_bssid = args.fake_ap_bssid
    packets_number = args.packets_number
    test_rounds_number = args.test_rounds_number

    for test_round in range(test_rounds_number):
        list_of_dict_time_real = start_live_capture(packets_number=packets_number,
                                                    dict_key_name=f"real ({real_ap_bssid})")

        list_of_dict_time_evil_twin = start_live_capture(packets_number=packets_number,
                                                         dict_key_name=f"evil_twin ({fake_ap_bssid})")

        list_of_dict_time_merged = merge_two_lists_of_dict(list_of_dict_time_real,
                                                           list_of_dict_time_evil_twin)

        # Creating Dataframe with merged times for both APs.
        df = pd.DataFrame(list_of_dict_time_merged)

        # In order to remove noised data, we filter outliers.
        df = filter_outliers(df)

        ax1 = df.plot(kind='scatter', x='index', y='real', color='g', label="real")
        ax2 = df.plot(kind='scatter', x='index', y='evil_twin', color='r', label="evil_twin",
                      ax=ax1)

        # print(df.mean(axis=0))
        # print(df.median(axis=0))
        plt.savefig(f"{time.time()}-{test_round}.png")
        plt.show()
