import sys
import os
sys.path.append("core_v3")
from bridges import IronBridges
from analytics import IronAnalytics

secrets_path = "core_v3/secrets.json"
bridges = IronBridges(secrets_path)

print("--- BINANCE DIAGNOSTIC ---")
if bridges.binance:
    print("API Handshake: SUCCESS")
    assets = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "DOGE/USDT"]
    for symbol in assets:
        try:
            er = IronAnalytics.get_efficiency_ratio(symbol, bridges=bridges)
            print(f"Asset: {symbol} | ER: {er:.4f}")
        except Exception as e:
            print(f"Asset: {symbol} | Error: {e}")
else:
    print("API Handshake: FAILED")
