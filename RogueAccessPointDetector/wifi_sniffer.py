import nmcli

for wifi_dev in nmcli.device.wifi():
    print(wifi_dev)
    nmcli.device