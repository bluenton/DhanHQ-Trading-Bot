import os
import requests
import time

# Load API credentials from GitHub Secrets
API_KEY = os.getenv("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM4MzExMzU4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDUxMjg1NyJ9.kGg4tZDEBWaDfW6bMlfCV-JZKk_Fy3Xu5-g31p-T19_nWc1Cj4EzzqbtsZZdrQcSSq85juxHwXzQotBjC1hfkQ")
CLIENT_ID = os.getenv("1104512857")

# Dhan API Base URL
BASE_URL = "https://api.dhan.co"

# Trading Parameters
OPTION_SYMBOL = "NSE_OPT_SBIN_900_FEB"  # SBIN 900 CALL Feb
TRADE_QUANTITY = 50  # Adjust as per lot size
STOP_LOSS_PERCENT = 10  # 10% stop-loss
TAKE_PROFIT_PERCENT = 25  # 25% take-profit

# Fetch live option price
def get_option_price(symbol):
    url = f"{BASE_URL}/market/v1/quote/{symbol}"
    headers = {
        "X-Dhan-Client-Id": CLIENT_ID,
        "X-Dhan-Auth-Token": API_KEY
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if "ltp" in data:
        return float(data["ltp"])
    else:
        print("Error fetching price:", data)
        return None

# Place option order
def place_order(symbol, quantity, order_type, price):
    url = f"{BASE_URL}/orders/v1/place/"
    headers = {
        "X-Dhan-Client-Id": CLIENT_ID,
        "X-Dhan-Auth-Token": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "security_id": symbol,
        "exchange_segment": "NSE_FNO",
        "transactionType": order_type,
        "quantity": quantity,
        "orderType": "LIMIT",  # Use LIMIT order
        "productType": "INTRADAY",
        "price": price  # Use live price for limit order
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    print(f"ORDER RESPONSE: {response_data}")
    
    if "order_id" in response_data:
        return response_data["order_id"]
    else:
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
    entry_price = get_option_price(OPTION_SYMBOL)
    if entry_price is None:
        print("Error fetching option price. Exiting.")
        return

    stop_loss_price = entry_price - (entry_price * STOP_LOSS_PERCENT / 100)
    take_profit_price = entry_price + (entry_price * TAKE_PROFIT_PERCENT / 100)

    print(f"Entry Price: {entry_price}, Stop Loss: {stop_loss_price}, Take Profit: {take_profit_price}")

    # Place buy order
    order_id = place_order(OPTION_SYMBOL, TRADE_QUANTITY, "BUY", entry_price)
    if order_id is None:
        print("Order Failed. Exiting.")
        return

    print(f"Buy Order Placed: {order_id}")

    # Monitor trade
    while True:
        current_price = get_option_price(OPTION_SYMBOL)
        if current_price is None:
            print("Error fetching price. Retrying...")
            time.sleep(10)
            continue

        print(f"Current Price: {current_price}")

        if current_price <= stop_loss_price:
            print("Stop-Loss hit. Selling position...")
            place_order(OPTION_SYMBOL, TRADE_QUANTITY, "SELL", current_price)
            break

        if current_price >= take_profit_price:
            print("Take-Profit reached. Selling position...")
            place_order(OPTION_SYMBOL, TRADE_QUANTITY, "SELL", current_price)
            break

        time.sleep(30)  # Check every 30 seconds

# Run bot
if __name__ == "__main__":
    auto_trade()
