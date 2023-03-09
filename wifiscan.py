#! /usr/bin/env python3


import subprocess


with open("/home/wifi_scan_result.txt", "w") as f:
    nmcli = subprocess.run(['nmcli', '-f', 'ALL', 'dev', 'wifi'], stdout=f, text=True)


with open("/home/wifi_scan_result2.txt", "w") as f:
    nmclii = subprocess.run(['nmcli', '-f', 'BSSID, SSID, CHAN, SECURITY, SIGNAL, BARS', 'd', 'wifi'], stdout=f, text=True)
