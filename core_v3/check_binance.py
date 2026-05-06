from bridges import IronBridges
import os

if __name__ == "__main__":
    try:
        secrets_path = os.path.join(os.path.dirname(__file__), "secrets.json")
        b = IronBridges(secrets_path)
        # Assuming b.binance is initialized in __init__ or via a property
        bal = b.binance.fetch_balance()
        print(f"USDT_TOTAL: {bal['total'].get('USDT', 0)}")
        print(f"USDT_FREE: {bal['free'].get('USDT', 0)}")
    except Exception as e:
        print(f"FAIL: {e}")
