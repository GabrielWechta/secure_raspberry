import sys

from scapy.layers.inet import IP, ICMP, sr1, RandShort, TCP, sr, socket, conf


def check_if_server_is_alive(destination_ip: str) -> bool:
    icmp_packet = IP(dst=destination_ip) / ICMP()
    icmp_response = sr1(icmp_packet, timeout=3)
    if icmp_response is None:
        return False
    else:
        return True


def syn_probe_port(destination_ip: str, destination_port: int) -> int:
    """
    Get status of given port.

    :param destination_ip: Server's IP address.
    :param destination_port: Server's port to test.
    :return:
     0 - for closed;
     1 - for open;
     2 - for filtered.
    """
    port_status = 0
    source_port = RandShort()
    try:
        packet = IP(dst=destination_ip) / TCP(sport=source_port, dport=destination_port, flags='S')
        synack_response = sr1(packet, timeout=2)  # Sending SYN, receiving SYNC/ACK.
        if synack_response is None:
            port_status = 0
        elif synack_response.haslayer(TCP):

            # This port is closed
            if synack_response.getlayer(TCP).flags == 0x14:  # It is RST/ACK
                port_status = 0

            # This port is open
            elif synack_response.getlayer(TCP).flags == 0x12:  # It is SYN
                _ = sr(IP(dst=destination_ip) / TCP(sport=source_port, dport=destination_port,
                                                    flags='AR'),
                       timeout=1)
                port_status = 1

            # This port is filtered
            elif int(synack_response.getlayer(ICMP).type) == 3 and int(
                    synack_response.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]:
                port_status = 2
    except ValueError as e:
        print(f"Error accrued during silent port scanning {e}.")

    return port_status


if __name__ == '__main__':
    conf.verb = 0

    host_name = sys.argv[1]
    server_ip = socket.gethostbyname(host_name)
    print(f"Server's ip: {server_ip}")

    open_ports = []
    filtered_ports = []
    common_ports = [21, 22, 23, 25, 53, 69, 80, 88, 109, 110, 123, 137, 138, 139, 143, 156, 161,
                    389, 443, 445, 500, 546, 547, 587, 660, 995, 993, 2086, 2087, 2082, 2083,
                    3306, 8443, 10000]

    if check_if_server_is_alive(server_ip):  # Send ICMP to check if host is up
        for port in common_ports:
            result = syn_probe_port(server_ip, port)
            if result == 1:
                open_ports.append(port)
            elif result == 2:
                filtered_ports.append(port)

        print(f"Open ports of {host_name}:", open_ports)
        print(f"Filtered ports of {host_name}:", filtered_ports)
    else:
        print("Host is down.")
