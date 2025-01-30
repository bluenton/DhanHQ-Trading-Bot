import os
import requests

# Load API credentials from environment variables
API_KEY = os.getenv("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM4MzExMzU4LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwNDUxMjg1NyJ9.kGg4tZDEBWaDfW6bMlfCV-JZKk_Fy3Xu5-g31p-T19_nWc1Cj4EzzqbtsZZdrQcSSq85juxHwXzQotBjC1hfkQ")
CLIENT_ID = os.getenv("1104512857")

# Dhan API Base URL
BASE_URL = "https://api.dhan.co"

# Function to fetch live price
def get_price(symbol="NSE_FUT_NIFTY_1M"):
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
        return None

# Function to place an order
def place_order(symbol="NSE_FUT_NIFTY_1M", quantity=1, order_type="BUY"):
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
        "orderType": "MARKET",
        "productType": "INTRADAY",
        "price": 0
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Test fetching price
if __name__ == "__main__":
    nifty_price = get_price()
    print(f"Live Nifty Futures Price: {nifty_price}")
    
    if nifty_price and nifty_price > 20000:
        print("Placing BUY Order...")
        response = place_order(order_type="BUY")
        print("Order Response:", response)
