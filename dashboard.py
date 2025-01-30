from flask import Flask, jsonify
import threading
import os
import requests
import time

app = Flask(__name__)

API_KEY = os.getenv("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM4MzExMzU4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDUxMjg1NyJ9.kGg4tZDEBWaDfW6bMlfCV-JZKk_Fy3Xu5-g31p-T19_nWc1Cj4EzzqbtsZZdrQcSSq85juxHwXzQotBjC1hfkQ")
CLIENT_ID = os.getenv("1104512857")
BASE_URL = "https://api.dhan.co"
OPTION_SYMBOL = "NSE_OPT_SBIN_900_FEB"

current_price = None
stop_loss = None
take_profit = None

def fetch_price():
    global current_price
    while True:
        url = f"{BASE_URL}/market/v1/quote/{OPTION_SYMBOL}"
        headers = {
            "X-Dhan-Client-Id": CLIENT_ID,
            "X-Dhan-Auth-Token": API_KEY
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        if "ltp" in data:
            current_price = float(data["ltp"])
        time.sleep(10)  # Fetch price every 10 seconds

@app.route('/status')
def status():
    return jsonify({
        "Current Price": current_price,
        "Stop Loss": stop_loss,
        "Take Profit": take_profit
    })

if __name__ == "__main__":
    price_thread = threading.Thread(target=fetch_price)
    price_thread.start()
    app.run(host="0.0.0.0", port=5000)
