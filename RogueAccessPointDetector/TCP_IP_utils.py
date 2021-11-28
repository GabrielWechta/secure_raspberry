from scapy.layers.inet import RandShort, IP, TCP, sr1


def start_3_way_handshake(destination_ip: str, destination_port: int) -> None:
    """
    Start 3-Way TCP Handshake, by sending SYN packet and receiving SYN/ACK. Most likely you OS
    will respond with RST not with ACK, but it is not important for this script. We only use
    information from the SYN/ACK packet.

    :param destination_ip: IP address of the server you want to connect to.
    :param destination_port: Server's port that you want to connect to
    """
    source_port = RandShort()
    try:
        # Building IP layer
        ip_layer = IP(dst=destination_ip)
        # Building TCP layer
        syn_tcp_layer = TCP(sport=source_port, dport=destination_port, flags='S')
        syn_packet_composed = ip_layer / syn_tcp_layer  # Connecting ip and tcp layer
        sr1(syn_packet_composed, timeout=1)  # Sending packet with expected receive
    except ValueError:
        print("Exception during 3 way handshake. You may need to run with root privileges.")
