import yfinance as yf
import requests
import os
from datetime import datetime

# --- CONFIGURATION ---
# PASTE YOUR DISCORD WEBHOOK URL HERE
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# YOUR WATCHLIST & TARGETS
WATCHLIST = {
    "VRTX": {"target": 450.50, "condition": "below", "msg": "🟢 BUY SIGNAL: Vertex hit limit price!"},
    "JD":   {"target": 30.00,  "condition": "below", "msg": "🔴 RISK ALERT: JD has dropped below support!"},
    "QQQ":  {"target": 480.00, "condition": "below", "msg": "⚠️ OPPORTUNITY: Market dip detected."},
    "CRWV": {"target": 65.00,  "condition": "below", "msg": "🚀 SIGNAL: CRWV below target!"}
}

def send_discord_alert(message):
    if not WEBHOOK_URL:
        print("Error: Webhook URL not found.")
        return
    data = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=data)
        print("Alert sent.")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def check_market():
    print(f"[{datetime.now().strftime('%H:%M')}] Checking markets...")

    tickers = list(WATCHLIST.keys())

    try:
        # Fetch data
        data = yf.download(tickers, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
 
        for ticker, rules in WATCHLIST.items():
            current_price = data[ticker]
            if (rules['condition'] == "below" and current_price <= rules['target']) or \
               (rules['condition'] == "above" and current_price >= rules['target']):
                
                msg = f"**{rules['msg']}**\n📊 **{ticker}** is now **${current_price:.2f}**"
                send_discord_alert(msg)
                
    except Exception as e:
        print(f"Error fetching data: {e}")

# --- MAIN LOOP ---
if __name__ == "__main__":
    check_market()