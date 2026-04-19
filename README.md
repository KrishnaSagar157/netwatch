# NetWatch – Real-Time Network Monitoring Dashboard

## Overview

NetWatch is a real-time network monitoring and analysis tool built using Python. It detects active devices on a local network, monitors changes (device join/leave events), performs port-based device analysis, and visualizes everything through a live web dashboard.

The project combines network scanning, event tracking, and a clean UI to provide visibility into network activity in a simple and practical way.

---

## Features

### Network Discovery

* Ping-based scanning to find all active IPs on the subnet
* ARP-based scanning to retrieve MAC addresses
* Monitor mode combines both for maximum device visibility

### Port Scanning

* Identifies open ports on discovered devices
* Uses multithreading for faster execution

### Device Identification

* Infers device type based on open ports
* MAC vendor lookup with per-session caching to avoid rate limits

### Real-Time Monitoring

* Continuously monitors network activity using combined ping + ARP scan
* Detects:
  * New devices (JOIN)
  * Disconnected devices (LEAVE) with debounce to avoid false alerts

### Event Logging

* Maintains event history (JOIN / LEAVE)
* Stores last 50 events

### Web Dashboard

* Live device table with:
  * IP, MAC, Open Ports, Device Type, Vendor
* Event log timeline with JOIN / LEAVE badges
* Auto-refresh every 10 seconds
* Clean dark-themed UI

### Alerts

* Visual indicators for new and suspicious devices
* Browser notifications for network events

---

## Dashboard Preview

![Dashboard](screenshots/dashboard.png)

---

## Project Structure

```text
netwatch/
│
├── main.py                  # Scanner and monitoring logic
├── app.py                   # Flask dashboard
│
├── scanner/
│   ├── arp_scanner.py       # ARP scan + targeted MAC lookup
│   ├── ping_scanner.py      # Ping-based IP discovery
│   └── port_scanner.py      # Port scanning + device type inference
│
├── utils/
│   ├── event_logger.py      # JOIN / LEAVE event logging
│   ├── output.py            # Save / load scan results
│   └── mac_lookup.py        # MAC vendor lookup with caching
│
├── templates/
│   └── index.html           # Dashboard UI
│
├── data/                    # Ignored (runtime data)
├── screenshots/             # UI images
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/KrishnaSagar157/netwatch.git
cd netwatch

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## Usage

### 1. Start Monitoring

```bash
sudo venv/bin/python main.py
```

Select scan type:

```
1 → Ping Scan       — finds active IPs only
2 → ARP Scan        — finds IPs + MAC addresses
3 → Monitor Mode    — combined ping + ARP, runs continuously
```

---

### 2. Start Dashboard

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## How It Works

1. **Ping scan** discovers all active IPs on the subnet
2. **ARP scan** retrieves MAC addresses via broadcast
3. For devices missed by ARP, a targeted ARP request is sent directly
4. Each device is analyzed — ports scanned, vendor looked up, device type inferred
5. Results are saved as JSON; empty scans are skipped
6. Monitor mode compares current vs previous scan to detect JOIN / LEAVE events
7. LEAVE events trigger after 1 missed cycle (~15 seconds) — combined scan reduces false alerts
8. Dashboard reads the latest scan file and updates automatically every 10 seconds

---

## Data Handling

* Scan results — stored as timestamped JSON files, capped at 20 files
* Event logs — last 50 entries kept
* Empty scans are never saved to prevent incorrect dashboard states
* MAC vendor results are cached per session to avoid API rate limits

---

## Limitations

* Works only within local network (ARP and ping based)
* Requires `sudo` for ARP scanning (raw packet access)
* Some devices may not respond to ping or ARP (firewalls, client isolation)
* Mobile hotspots may hide connected devices from ARP

---

## Highlights

* Combined ping + ARP scanning for maximum device discovery
* Debounced LEAVE detection to reduce false alerts from unstable ARP responses
* Modular Python architecture — scanners, utils, and dashboard are fully separated
* MAC vendor caching to avoid rate limiting during continuous monitoring
* Live Flask dashboard with event badges, port tags, and browser notifications

---

## Resume Description

Developed NetWatch, a real-time network monitoring system using Python that combines ping and ARP-based device discovery, multithreaded port scanning, and MAC vendor fingerprinting. Implemented debounced event detection for device join/leave events and built a Flask dashboard with live updates, browser notifications, and structured network visualization.

---

## License

This project is for educational and personal use.
