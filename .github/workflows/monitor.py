import urllib.request
import json
import os
import time

TARGET = 0.01
TG_TOKEN = os.environ["TG_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

API_URL = "https://api-airdrop.river.inc/s2/pts-conversion-chart?interval=1d"


def fetch():
    for i in range(3):
        try:
            req = urllib.request.Request(API_URL, headers={"Cache-Control": "no-store"})
            with urllib.request.urlopen(req, timeout=10) as res:
                return json.loads(res.read())
        except Exception as e:
            print("retry:", e)
            time.sleep(2)
    return None


data = fetch()

if not data:
    print("API error")
    exit()

valid = [x for x in data["data"] if x["actualRate"] is not None]

if not valid:
    print("No data")
    exit()

last = valid[-1]

actual = float(last["actualRate"])
ideal = float(last["expectedRate"])

print("Actual:", actual)
print("Ideal:", ideal)

if actual >= TARGET:
    message = f"""
🚨 River Airdrop 목표 도달!

Actual Rate : {actual:.6f}
Target      : {TARGET}

🔥 Target reached
"""
else:
    message = f"""
📊 River Conversion Update

Actual Rate : {actual:.6f}
Ideal Rate  : {ideal:.6f}
Target      : {TARGET}

⏱ Update every 5 minutes
"""

tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"

body = json.dumps({
    "chat_id": CHAT_ID,
    "text": message
}).encode()

req = urllib.request.Request(
    tg_url,
    data=body,
    headers={"Content-Type": "application/json"},
    method="POST"
)

urllib.request.urlopen(req)

print("telegram sent")
