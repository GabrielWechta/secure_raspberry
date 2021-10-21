import sys

from scapy.layers.inet import *


def is_up(ip):
    icmp = IP(dst=ip) / ICMP()
    resp = sr1(icmp, timeout=3)
    return False if resp is None else True


def probe_port(ip, destination_port, result=1):
    source_port = RandShort()
    try:
        p = IP(dst=ip) / TCP(sport=source_port, dport=destination_port, flags='S')
        resp = sr1(p, timeout=2)  # Sending packet
        if resp is None:
            result = 0
        elif resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x12:  # It is SYN
                _ = sr(IP(dst=ip) / TCP(sport=source_port, dport=destination_port, flags='AR'), timeout=1)
                result = 1
            elif resp.getlayer(TCP).flags == 0x14:  # It is RST/ACK
                result = 0
            elif int(resp.getlayer(ICMP).type) == 3 and int(resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]:
                result = 2
    except Exception as e:
        pass

    return result


if __name__ == '__main__':
    host = sys.argv[1]
    ip = socket.gethostbyname(host)
    print(f"Host's ip: {ip}")

    open_ports = []
    filtered_ports = []
    common_ports = [21, 22, 23, 25, 53, 69, 80, 88, 109, 110, 123, 137, 138, 139, 143, 156, 161, 389, 443,
                    445, 500, 546, 547, 587, 660, 995, 993, 2086, 2087, 2082, 2083, 3306, 8443, 10000]

    conf.verb = 0
    if is_up(ip):  # Send ICMP to check if host i up
        for port in common_ports:
            print(port)
            response = probe_port(ip, port)
            if response == 1:
                open_ports.append(port)
            elif response == 2:
                filtered_ports.append(port)

        if open_ports:
            print("Open Ports:")
            print(open_ports)
        else:
            print("I didn't find any open ports. Try specifying bigger set.")

        if len(filtered_ports) != 0:
            print("Possible Filtered Ports:")
            print(filtered_ports)
    else:
        print("Host is Down")
