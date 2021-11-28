import argparse
import time

import network_manager_utils
from TCP_IP_utils import start_3_way_handshake
from testing_new_tcp import do_3_way


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This script connects to server using TCP connection. In order to keep "
                    "separate environment for scapy it will be run as separate process."
    )

    parser.add_argument(
        "--target_bssid",
        dest="target_bssid",
        type=str,
        help="BSSID for target Access Point.",
    )

    parser.add_argument(
        "--destination_ip",
        dest="destination_ip",
        type=str,
        help="Server's IP address.",
    )

    parser.add_argument(
        "--destination_port",
        dest="destination_port",
        type=int,
        help="Server's port.",
    )

    parser.add_argument(
        "--packets_number",
        dest="packets_number",
        type=int,
        help="Number of packets that will be sent to server.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    target_bssid = args.target_bssid
    destination_port = args.destination_port
    destination_ip = args.destination_ip
    packets_number = args.packets_number

    # network_manager_utils.connect_to_network_by_bssid(target_bssid)

    for i in range(packets_number):
        start_3_way_handshake(destination_ip=destination_ip, destination_port=destination_port)
        time.sleep(0.1)
