import socket
from concurrent.futures import ThreadPoolExecutor

def scan_single_port(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    result = s.connect_ex((ip, port))
    s.close()

    if result == 0:
        return port
    return None


def scan_ports(ip):
    common_ports = [21, 22, 23, 53, 80, 135, 139, 443, 445, 3389, 8080]
    open_ports = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(lambda port, ip=ip: scan_single_port(ip, port), common_ports)

    for port in results:
        if port:
            open_ports.append(port)

    return open_ports

def guess_device(ports, vendor):
    if "Amazon" in vendor:
        return "Cloud / AWS Device ☁️"
    elif 53 in ports:
        return "DNS Server / Router 🌐"
    elif 80 in ports or 443 in ports:
        return "Web Server / Router 🖥️"
    elif 22 in ports:
        return "Linux Device 🐧"
    elif 3389 in ports:
        return "Windows Machine 🪟"
    elif len(ports) == 0:
        return "Hidden / Firewalled Device 🔒"
    else:
        return "Unknown Device ❓"
