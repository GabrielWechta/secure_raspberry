import socket
import sys


def probe_port(host, port, result=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    r = sock.connect_ex((host, port))
    if r == 0:
        result = r

    sock.close()
    return result


if __name__ == "__main__":
    host = sys.argv[1]
    open_ports = []
    common_ports = [21, 22, 23, 25, 53, 69, 80, 88, 109, 110, 123, 137, 138, 139, 143, 156, 161, 389, 443, 445, 500,
                    546, 547, 587, 660, 995, 993, 2086, 2087, 2082, 2083, 2222, 3306, 8443, 10000]
    ip = socket.gethostbyname(host)
    print(f"Host's ip: {ip}")

    for port in sorted(common_ports):
        response = probe_port(host, port)
        if response == 0:
            open_ports.append(port)

    if open_ports:
        print("Open Ports:")
        print(open_ports)
    else:
        print("I didn't find any open ports. Try specifying bigger set.")
