import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

def save_results(data):
    if not data:
        print("Empty scan — skipping save.")
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    filename = os.path.join(DATA_DIR, f"scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    scan_files = [f for f in sorted(os.listdir(DATA_DIR)) if f.startswith("scan_")]

    if len(scan_files) >= 20:
        os.remove(os.path.join(DATA_DIR, scan_files[0]))

    with open(filename, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\n Results saved to {filename}")


def load_last_scan():
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        scan_files = [f for f in sorted(os.listdir(DATA_DIR)) if f.startswith("scan_")]
        if not scan_files:
            return []
        with open(os.path.join(DATA_DIR, scan_files[-1]), "r") as f:
            return json.load(f)
    except:
        return []

def detect_new_devices(old, new):
    old_ips = {device["ip"] for device in old}
    return [device for device in new if device["ip"] not in old_ips]

def detect_left_devices(old, new):
    new_ips = {device["ip"] for device in new}
    return [device for device in old if device["ip"] not in new_ips]
