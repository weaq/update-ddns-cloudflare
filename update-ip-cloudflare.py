#!/usr/bin/env python3
import requests
import sys
import time
from datetime import datetime

# ================= CONFIG =================
CF_API_TOKEN = "YOUR_API_TOKEN"   # ใช้ API Token (แนะนำ)
ZONE_ID = "YOUR_ZONE_ID"
DOMAIN = "weaq.cc"
RECORD_NAME = "weaq.cc"   # root domain

IP_API = "https://api.ipify.org?format=json"

HEADERS = {
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json"
}

# ================= LOG =================
def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# ================= GET PUBLIC IP =================
def get_public_ip():
    for i in range(3):
        try:
            r = requests.get(IP_API, timeout=5)
            r.raise_for_status()
            return r.json()["ip"]
        except Exception as e:
            log(f"Retry get IP ({i+1}/3): {e}")
            time.sleep(2)
    return None

# ================= GET DNS RECORD =================
def get_dns_record():
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records?name={RECORD_NAME}"
    r = requests.get(url, headers=HEADERS)
    data = r.json()

    if not data.get("success") or not data["result"]:
        log(f"❌ Failed to get DNS record: {data}")
        return None

    return data["result"][0]

# ================= UPDATE DNS =================
def update_dns(record_id, ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}"

    payload = {
        "type": "A",
        "name": RECORD_NAME,
        "content": ip,
        "ttl": 120,
        "proxied": True   # ถ้าใช้ Cloudflare proxy เปลี่ยนเป็น True
    }

    r = requests.put(url, headers=HEADERS, json=payload)
    data = r.json()

    if not data.get("success"):
        log(f"❌ Update failed: {data}")
        return False

    log(f"✅ Updated {RECORD_NAME} -> {ip}")
    return True

# ================= MAIN =================
def main():
    log("=== DDNS UPDATE START ===")

    ip = get_public_ip()
    if not ip:
        log("❌ Cannot get public IP")
        sys.exit(1)

    log(f"🌐 Current Public IP: {ip}")

    record = get_dns_record()
    if not record:
        sys.exit(1)

    record_id = record["id"]
    current_ip = record["content"]

    log(f"📡 DNS IP: {current_ip}")

    if current_ip == ip:
        log("✅ IP unchanged. Skip update.")
        return

    log("⚠️ IP changed! Updating...")
    update_dns(record_id, ip)


if __name__ == "__main__":
    main()