import argparse
import time
from datetime import datetime

import pandas as pd
from matplotlib import pyplot as plt

plt.style.use('ggplot')
from TCP_IP_utils import start_3_way_handshake
from capture_utils import start_live_capture, merge_two_lists_of_dict, filter_outliers


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This program executes tests for EvilTwinDetector."
    )

    parser.add_argument(
        "--legal_ap_bssid",
        dest="legal_ap_bssid",
        type=str,
        help="BSSID for true/valid Access Point.",
    )

    parser.add_argument(
        "--evil_twin_ap_bssid",
        dest="evil_twin_ap_bssid",
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


def execute_test_on_ap(number_of_packets: int, target_bssid: str, destination_ip: str,
                       destination_port: int) -> None:
    print("dupa")
    for _ in range(number_of_packets):
        start_3_way_handshake(destination_ip=destination_ip, destination_port=destination_port)
        time.sleep(0.1)
    print(f"finished for {target_bssid}")


if __name__ == "__main__":
    args = _parse_args()
    legal_ap_bssid = args.legal_ap_bssid
    evil_twin_ap_bssid = args.evil_twin_ap_bssid
    packets_number = args.packets_number
    test_rounds_number = args.test_rounds_number

    for test_round in range(1):
        """ Getting data for legal Access Point. """
        print("start")
        list_of_dict_time_legal = start_live_capture(packets_number, f"Legal",
                                                     "wlp4s0")
        print("legal")

        """ Getting data for ET Access Point. """
        list_of_dict_time_evil_twin = start_live_capture(packets_number, f"Evil Twin",
                                                         "wlp4s0")
        print("ET")

        """ Merging data from both AP. """
        list_of_dict_time_merged = merge_two_lists_of_dict(list_of_dict_time_legal,
                                                           list_of_dict_time_evil_twin)

        # Creating Dataframe with merged times for both APs.
        df = pd.DataFrame(list_of_dict_time_merged)

        # In order to remove noised data, we filter outliers.
        df = filter_outliers(df)

        ax1 = df.plot(kind='scatter', x='index', y=f"Legal", color='g', label="Legal")
        ax2 = df.plot(kind='scatter', x='index', y=f"Evil Twin", color='r',
                      label="Evil Twin",
                      ax=ax1)
        plt.ylabel("time [s]")

        print(df.mean(axis=0))
        print(df.median(axis=0))
        with open("results.txt", "a") as result_file:
            result_file.write(str(df[["Legal", "Evil Twin"]].mean(axis=0)))
            result_file.write(str(df[["Legal", "Evil Twin"]].median(axis=0)))

        plt.savefig(f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}-{test_round}.png",
                    format="eps")
        plt.show()
