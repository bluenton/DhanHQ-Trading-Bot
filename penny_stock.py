import os
import requests
import time

# Load API credentials from GitHub Secrets
API_KEY = os.getenv("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM4MzExMzU4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDUxMjg1NyJ9.kGg4tZDEBWaDfW6bMlfCV-JZKk_Fy3Xu5-g31p-T19_nWc1Cj4EzzqbtsZZdrQcSSq85juxHwXzQotBjC1hfkQ")
CLIENT_ID = os.getenv("1104512857")

# Dhan API Base URL
BASE_URL = "https://api.dhan.co"

# Trading Parameters
SECURITY_ID = "1168501"  # ✅ Correct security ID for Vodafone Idea (IDEA)
TRADE_QUANTITY = 100  # Buy 100 shares
STOP_LOSS_PERCENT = 5  # 5% stop-loss
TAKE_PROFIT_PERCENT = 10  # 10% take-profit

# Fetch live stock price
def get_stock_price(security_id):
    url = f"{BASE_URL}/market/v1/quote/{security_id}"
    headers = {
        "X-Dhan-Client-Id": CLIENT_ID,
        "X-Dhan-Auth-Token": API_KEY
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if "ltp" in data:
        return float(data["ltp"])
    else:
        print("⚠️ Error fetching price:", data)
        return None

# Place stock order
def place_order(security_id, quantity, order_type, price):
    url = f"{BASE_URL}/orders/v1/place/"
    headers = {
        "X-Dhan-Client-Id": CLIENT_ID,
        "X-Dhan-Auth-Token": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "security_id": security_id,
        "exchange_segment": "NSE_EQ",
        "transactionType": order_type,
        "quantity": quantity,
        "orderType": "LIMIT",  # Use LIMIT order
        "productType": "INTRADAY",
        "price": price
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    print(f"ORDER RESPONSE: {response_data}")
    
    if "order_id" in response_data:
        return response_data["order_id"]
    else:
        print("⚠️ Order Failed:", response_data)
        return None

# Fetch order status
def get_order_status(order_id):
    url = f"{BASE_URL}/orders/v1/order/{order_id}"
    headers = {
        "X-Dhan-Client-Id": CLIENT_ID,
        "X-Dhan-Auth-Token": API_KEY
    }

    response = requests.get(url, headers=headers)
    return response.json()

# Automated trading with stop-loss & take-profit
def auto_trade():
    entry_price = get_stock_price(SECURITY_ID)
    if entry_price is None:
        print("⚠️ Error fetching stock price. Exiting.")
        return

    stop_loss_price = entry_price - (entry_price * STOP_LOSS_PERCENT / 100)
    take_profit_price = entry_price + (entry_price * TAKE_PROFIT_PERCENT / 100)

    print(f"Entry Price: {entry_price}, Stop Loss: {stop_loss_price}, Take Profit: {take_profit_price}")

    # Place buy order
    order_id = place_order(SECURITY_ID, TRADE_QUANTITY, "BUY", entry_price)
    if order_id is None:
        print("⚠️ Order Failed. Exiting.")
        return

    print(f"✅ Buy Order Placed: {order_id}")

    # Monitor trade
    while True:
        current_price = get_stock_price(SECURITY_ID)
        if current_price is None:
            print("⚠️ Error fetching price. Retrying...")
            time.sleep(10)
            continue

        print(f"📈 Current Price: {current_price}")

        if current_price <= stop_loss_price:
            print("❌ Stop-Loss hit. Selling position...")
            place_order(SECURITY_ID, TRADE_QUANTITY, "SELL", current_price)
            break

        if current_price >= take_profit_price:
            print("✅ Take-Profit reached. Selling position...")
            place_order(SECURITY_ID, TRADE_QUANTITY, "SELL", current_price)
            break

        time.sleep(30)  # Check every 30 seconds

# Run bot
if __name__ == "__main__":
    auto_trade()
