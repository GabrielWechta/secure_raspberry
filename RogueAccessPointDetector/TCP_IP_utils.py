from scapy.layers.inet import *
from scapy.all import send
import netifaces


# source_port = random.randint(1024, 65535)
#
# # SYN
# ip = IP(src='172.16.120.5', dst='172.16.100.101')
# SYN = TCP(sport=source_port, dport=443, flags='S', seq=1000)
# SYNACK = sr1(ip / SYN)
#
# # SYN-ACK
# ACK = TCP(sport=source_port, dport=443, flags='A', seq=SYNACK.ack + 1, ack=SYNACK.seq + 1)
# send(ip / ACK)



def start_3_way_handshake(destination_ip, destination_port):
    result = -1
    source_port = RandShort()
    try:
        ip_layer = IP(dst=destination_ip)
        timestamp = time.time()
        syn_tcp_layer = TCP(sport=source_port, dport=destination_port, flags='S')
        syn_packet_composed = ip_layer / syn_tcp_layer
        synack_response = sr1(syn_packet_composed, timeout=10)  # Sending packet
        print(synack_response.time - timestamp)

        if synack_response is None:
            result = 0
        else:
            ack_tcp_layer = TCP(sport=source_port, dport=destination_port, flags='A',
                                seq=synack_response.ack + 1, ack=synack_response.seq + 1)
            ack_packet_composed = ip_layer / ack_tcp_layer
            # _ = sr(ack_packet_composed, timeout=10)
            result = 1
    except Exception as e:
        print("Exception during 3 way handshake.")

    return result
