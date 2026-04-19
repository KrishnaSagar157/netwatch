from flask import Flask, render_template, jsonify
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

app = Flask(__name__)

def load_events():
    try:
        with open(os.path.join(DATA_DIR, "events.json")) as f:
            return json.load(f)[::-1]
    except:
        return []

def load_latest_with_flag():
    if not os.path.exists(DATA_DIR):
        return [], [], []

    scan_files = [f for f in sorted(os.listdir(DATA_DIR)) if f.startswith("scan_")]

    if not scan_files:
        return [], [], []

    with open(os.path.join(DATA_DIR, scan_files[-1])) as f:
        current = json.load(f)

    if not current:
        return [], [], []

    if len(scan_files) > 1:
        with open(os.path.join(DATA_DIR, scan_files[-2])) as f:
            previous = json.load(f)
        prev_ips = {d["ip"] for d in previous}
        new_ips = [d["ip"] for d in current if d["ip"] not in prev_ips]
    else:
        new_ips = []

    suspicious = [
        d for d in current
        if "Unknown" in d.get("device", "") or "Hidden" in d.get("device", "")
    ]

    return current, new_ips, suspicious

@app.route("/")
def index():
    devices, new_ips, suspicious = load_latest_with_flag()
    events = load_events()
    return render_template("index.html",
        devices=devices,
        new_ips=new_ips,
        suspicious=suspicious,
        events=events
    )

@app.route("/events")
def get_events():
    return jsonify(load_events())

if __name__ == "__main__":
    app.run(debug=True)
