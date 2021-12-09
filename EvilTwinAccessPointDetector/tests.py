import argparse
import csv
from datetime import datetime

import pandas as pd
from matplotlib import pyplot as plt

from capture_utils import start_live_capture, merge_two_lists_of_dict, filter_outliers


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This program executes tests for EvilTwinDetector."
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
        help="Number of testing rounds.",
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

    parser.add_argument(
        "--wireless_network_interface",
        dest="wireless_network_interface",
        default=None,
        type=str,
        help="Identifier for wireless network interface.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    packets_number = args.packets_number
    destination_ip = args.destination_ip
    destination_port = args.destination_port
    test_rounds_number = args.test_rounds_number
    wireless_network_interface = args.wireless_network_interface

    for test_round in range(test_rounds_number):
        """ Getting data for legal Access Point. """
        print("start legal")
        list_of_dict_time_legal = start_live_capture(packets_number=packets_number,
                                                     dict_key_name=f"Legal",
                                                     destination_ip=destination_ip,
                                                     destination_port=destination_port,
                                                     wireless_network_interface=wireless_network_interface)
        print("finished legal")

        """ Getting data for ET Access Point. """
        print("start ET")
        list_of_dict_time_evil_twin = start_live_capture(packets_number=packets_number,
                                                         dict_key_name=f"Evil Twin",
                                                         destination_ip=destination_ip,
                                                         destination_port=destination_port,
                                                         wireless_network_interface=wireless_network_interface)
        print("finished ET")

        # Merging data from both AP.
        list_of_dict_time_merged = merge_two_lists_of_dict(list_of_dict_time_legal,
                                                           list_of_dict_time_evil_twin)

        # Creating Dataframe with merged times for both APs.
        df = pd.DataFrame(list_of_dict_time_merged)

        # In order to remove noised data, we filter outliers.
        df = filter_outliers(df)

        # Plotting results.
        ax1 = df.plot(kind='scatter', x='index', y=f"Legal", color='g', label="Legal")
        ax2 = df.plot(kind='scatter', x='index', y=f"Evil Twin", color='r',
                      label="Evil Twin",
                      ax=ax1)
        plt.ylabel("time [s]")

        means = df[["Legal", "Evil Twin"]].mean(axis=0).values
        medians = df[["Legal", "Evil Twin"]].median(axis=0).values
        legal_mean, evil_twin_mean = means[0], means[1]
        legal_median, evil_twin_median = medians[0], medians[1]

        print(df[["Legal", "Evil Twin"]].mean(axis=0))
        print(df[["Legal", "Evil Twin"]].median(axis=0))

        # Row is entry for csv file, it follows pattern (num, num, bool, num, num bool].
        row = [legal_mean, evil_twin_mean, 1 if evil_twin_mean > legal_mean else 0,
               legal_median, evil_twin_median, 1 if evil_twin_median > legal_median else 0]

        with open('results.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)

        plt.savefig(f"plots/{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}-{test_round}.eps",
                    format="eps")
        # plt.show()
