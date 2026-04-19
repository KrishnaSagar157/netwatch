import os
import platform
from concurrent.futures import ThreadPoolExecutor

def scan_network(base_ip):
    active_devices = []

    def scan_ip(target_ip):
        if platform.system().lower() == "windows":
            cmd = f"ping -n 1 -w 1000 {target_ip} > nul"
        else:
            cmd = f"ping -c 1 -W 1 {target_ip} > /dev/null 2>&1"

        response = os.system(cmd)

        if response == 0:
            print(f"[+] Device found: {target_ip}")
            active_devices.append(target_ip)

    with ThreadPoolExecutor(max_workers=50) as executor:
        for i in range(1, 255):
            target_ip = base_ip + str(i)
            executor.submit(scan_ip, target_ip)

    return active_devices
