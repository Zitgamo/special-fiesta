import MetaTrader5 as mt5
import json
import os
from datetime import datetime, timedelta

def check_real_history():
    with open("core_v3/secrets_real.json", "r") as f:
        secrets = json.load(f)
    
    if not mt5.initialize():
        print("MT5 Init Failed")
        return

    if not mt5.login(secrets['login'], password=secrets['password'], server=secrets['server']):
        print("MT5 Login Failed")
        return

    # Check last 24 hours
    from_date = datetime.now() - timedelta(hours=24)
    to_date = datetime.now()
    
    deals = mt5.history_deals_get(from_date, to_date)
    if deals:
        print(f"FOUND {len(deals)} DEALS IN LAST 24H")
        print("SYMBOL | TYPE | VOLUME | PRICE | PROFIT | TIME")
        print("-" * 60)
        for d in deals:
            # Type 0=Buy, 1=Sell
            t_type = "BUY" if d.type == 0 else "SELL"
            time_str = datetime.fromtimestamp(d.time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{d.symbol} | {t_type} | {d.volume} | {d.price} | {d.profit} | {time_str}")
    else:
        print("NO DEALS FOUND IN HISTORY")

    mt5.shutdown()

if __name__ == "__main__":
    check_real_history()
