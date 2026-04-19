import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVENT_FILE = os.path.join(BASE_DIR, "data", "events.json")

def log_event(event_type, device):
    os.makedirs(os.path.dirname(EVENT_FILE), exist_ok=True)

    event = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "type": event_type,
        "ip": device["ip"],
        "mac": device["mac"],
        "device": device.get("device", "Unknown")
    }

    try:
        with open(EVENT_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(event)
    data = data[-50:]

    with open(EVENT_FILE, "w") as f:
        json.dump(data, f, indent=4)
