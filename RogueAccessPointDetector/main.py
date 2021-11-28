import subprocess
import time

if __name__ == "__main__":
    subprocess.call(
        "python tcp_flood.py --target_bssid 64:66:B3:1E:26:EF --destination_ip "
        "212.82.100.150 "
        "--destination_port 80 --packets_number 10")

    print("finished")
    time.sleep(3)
    subprocess.call(
        "python3 tcp_flood.py --target_bssid 6C:60:EB:87:88:99 --destination_ip 212.82.100.150 "
        "--destination_port 80 --packets_number 10")
