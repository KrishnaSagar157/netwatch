from scapy.all import ARP, Ether, srp

def scan_network_arp(base_ip):
    target_range = base_ip + "0/24"

    # Create ARP request
    arp = ARP(pdst=target_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether / arp

    result = srp(packet, timeout=2, verbose=0)[0]

    devices = []

    for sent, received in result:
        device_info = {
            "ip": received.psrc,
            "mac": received.hwsrc
        }
        print(f"[+] {received.psrc} → {received.hwsrc}")
        devices.append(device_info)

    return devices

def get_mac_for_ip(ip):
    """Targeted ARP for a single IP"""
    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    result = srp(ether/arp, timeout=1, verbose=0)[0]

    for sent, received in result:
        return received.hwsrc

    return "Unknown"
