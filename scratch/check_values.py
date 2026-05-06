import requests
import json

try:
    r = requests.get('http://127.0.0.1:5050/api/telemetry')
    data = r.json()
    print(f"Status: {data.get('status')}")
    print(f"Session PnL USD: {data.get('session_pnl_usd')}")
    print(f"Session PnL VND: {data.get('session_pnl_vnd')}")
    print(f"MT5 Equity: {data.get('health_mt5', {}).get('equity')}")
    print(f"MT5 Balance: {data.get('health_mt5', {}).get('balance')}")
except Exception as e:
    print(f"Error: {e}")
