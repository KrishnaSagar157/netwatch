from scanner.ping_scanner import scan_network
from scanner.arp_scanner import scan_network_arp, get_mac_for_ip
from scanner.port_scanner import scan_ports,guess_device
from utils.mac_lookup import get_vendor
from utils.output import save_results, load_last_scan, detect_new_devices, detect_left_devices
from utils.event_logger import log_event

ip = input("Enter your IP (e.g., 192.168.1.5): ")

parts = ip.split(".")
base_ip = parts[0] + "." + parts[1] + "." + parts[2] + "."

# Choose scan type
choice = input("Choose scan type (1 = Ping, 2 = ARP, 3 = Monitor): ")

if choice == "1":
    devices = scan_network(base_ip)

    print("\n====== Ping Scan Complete ======")
    print(f"Devices found: {len(devices)}\n")

    for device in devices:
        print(f"→ {device}")

elif choice == "2":
    devices = scan_network_arp(base_ip)

    print("\n====== ARP Scan Complete ======")
    print(f"Devices found: {len(devices)}\n")

    results = []

    for d in devices:
        ports = scan_ports(d['ip'])
        vendor = get_vendor(d['mac'])
        device_type = guess_device(ports, vendor)

        print(f"{d['ip']} → {d['mac']} | {ports} | {device_type} | {vendor}")

        results.append({
            "ip": d['ip'],
            "mac": d['mac'],
            "ports": ports,
            "device": device_type,
            "vendor": vendor
        })
    previous = load_last_scan()
    new_devices = detect_new_devices(previous, results)

    if new_devices:
        print("\n New devices detected:")
        for d in new_devices:
            print(f" {d['ip']} → {d['mac']} ({d['device']})")
    else:
        print("\nNo new devices detected ")
    save_results(results)

elif choice == "3":
    import time

    previous = load_last_scan()
    absent_counts = {}
    LEAVE_THRESHOLD = 1

    print("\n Smart monitoring started... (Ctrl+C to stop)\n")

    while True:
        # Combined scan — same logic as option 2
        ping_ips = scan_network(base_ip)
        arp_devices = scan_network_arp(base_ip)
        mac_map = {d['ip']: d['mac'] for d in arp_devices}

        results = []
        for ip in ping_ips:
            if ip in mac_map:
                mac = mac_map[ip]
            else:
                mac = get_mac_for_ip(ip)  # targeted ARP fallback

            ports = scan_ports(ip)
            vendor = get_vendor(mac)
            device_type = guess_device(ports, vendor)

            results.append({
                "ip": ip,
                "mac": mac,
                "ports": ports,
                "device": device_type,
                "vendor": vendor
            })

        if not results:
            print("Empty scan skipped")
            time.sleep(10)
            continue

        # NEW DEVICES
        new_devices = detect_new_devices(previous, results)
        if new_devices:
            print("\n New devices detected:")
            for d in new_devices:
                print(f" {d['ip']} → {d['mac']} ({d['device']})")
                log_event("JOIN", d)
                absent_counts.pop(d['ip'], None)  # Reset if it came back

        # DEBOUNCED LEAVE DETECTION
        current_ips = {d['ip'] for d in results}
        for d in previous:
            if d['ip'] not in current_ips:
                absent_counts[d['ip']] = absent_counts.get(d['ip'], 0) + 1
                if absent_counts[d['ip']] >= LEAVE_THRESHOLD:
                    print(f"\n Device left: {d['ip']} → {d['mac']}")
                    log_event("LEAVE", d)
                    absent_counts.pop(d['ip'])
            else:
                absent_counts.pop(d['ip'], None)  # Present, reset counter

        save_results(results)
        previous = results
        time.sleep(15)

else:
    print("Invalid choice ")
