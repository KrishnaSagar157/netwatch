import requests

_cache = {}

def get_vendor(mac):
    if mac in _cache:
        return _cache[mac]
    try:
        url = f"https://api.macvendors.com/{mac}"
        response = requests.get(url, timeout=2)
        vendor = response.text if response.status_code == 200 else "Unknown Vendor"
    except:
        vendor = "Lookup Failed"
    
    _cache[mac] = vendor
    return vendor
