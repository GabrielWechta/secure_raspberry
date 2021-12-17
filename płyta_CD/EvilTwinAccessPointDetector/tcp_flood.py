import argparse
import time

from TCP_IP_utils import start_3_way_handshake


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="This script connects packets_number-times to server using TCP connection. In "
                    "order to keep separate environment for scapy it is run as a separate process."
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

    for i in range(packets_number):
        start_3_way_handshake(destination_ip=destination_ip, destination_port=destination_port)
        # In order to keep remote server from recognising this behavior as TCP Flood attack we wait
        # for some time before sending next packet.
        time.sleep(0.1)
