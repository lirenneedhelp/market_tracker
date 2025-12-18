import yfinance as yf
import requests
import time
from datetime import datetime

# --- CONFIGURATION ---
# PASTE YOUR DISCORD WEBHOOK URL HERE
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1451055009994113094/UFAcQQ1ZZASwQRyYWhk4GLyOpN5GBDViu4mx5lTCsmdTrUhsU5MPGt5wzJArTdSoU-aw"

# YOUR WATCHLIST & TARGETS
WATCHLIST = {
    "VRTX": {"target": 450.50, "condition": "below", "msg": "🟢 BUY SIGNAL: Vertex hit limit price!"},
    "JD":   {"target": 30.00,  "condition": "below", "msg": "🔴 RISK ALERT: JD has dropped below support!"},
    "QQQ":  {"target": 480.00, "condition": "below", "msg": "⚠️ OPPORTUNITY: Market dip detected."},
    "CRWV": {"target": 65.00,  "condition": "below", "msg": "🚀 SIGNAL: CRWV below target!"}
}

def send_discord_alert(message):
    """Sends a message to your Discord channel."""
    data = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
        print(f"Alert sent: {message}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def check_market():
    print(f"[{datetime.now().strftime('%H:%M')}] Checking markets...")
    
    # 1. Get data for all tickers at once
    tickers = list(WATCHLIST.keys())
    try:
        data = yf.download(tickers, period="1d", interval="1m", progress=False)['Close'].iloc[-1]
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # 2. Compare prices to your targets
    for ticker, rules in WATCHLIST.items():
        current_price = data[ticker]
        target_price = rules['target']
        condition = rules['condition']
        
        # Logic check
        triggered = False
        if condition == "below" and current_price <= target_price:
            triggered = True
        elif condition == "above" and current_price >= target_price:
            triggered = True
            
        if triggered:
            # Format the message (Bold ticker, price)
            alert_msg = f"**{rules['msg']}**\n📊 **{ticker}** is now **${current_price:.2f}** (Target: ${target_price})"
            send_discord_alert(alert_msg)

# --- MAIN LOOP ---
if __name__ == "__main__":
    send_discord_alert("🤖 Portfolio Watchdog is ONLINE and monitoring...")
    
    while True:
        check_market()
        # Sleep for 15 minutes (900 seconds) to avoid spamming
        time.sleep(900)