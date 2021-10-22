from time import sleep

from TCP_IP_utils import start_3_way_handshake

if __name__ == "__main__":
    for i in range(10):
        start_3_way_handshake('172.217.16.3', 80)