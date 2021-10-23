from time import sleep

import network_manager_utils
from TCP_IP_utils import start_3_way_handshake

if __name__ == "__main__":
    for i in range(100):
        start_3_way_handshake('172.217.16.3', 80)

    sleep(2)

    network_manager_utils.connect_to_network_by_bssid("6C:60:EB:87:88:99")

    sleep(4)

    for i in range(100):
        start_3_way_handshake('172.217.16.3', 80)

    network_manager_utils.connect_to_network_by_bssid("64:66:B3:1E:26:EF")

