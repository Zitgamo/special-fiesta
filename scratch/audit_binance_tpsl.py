import sys
import os
sys.path.append("core_v3")
from bridges import IronBridges

secrets_path = "core_v3/secrets.json"
bridges = IronBridges(secrets_path)

if bridges.binance:
    print("--- BINANCE SL/TP AUDIT ---")
    positions = bridges.binance.fetch_positions()
    for p in positions:
        vol = float(p['contracts'])
        if vol == 0: continue
        
        symbol = p['symbol'].split(':')[0]
        side = p['side'].upper()
        print(f"Position: {symbol} | Side: {side} | Amount: {vol}")
        
        # Check open orders for this symbol
        orders = bridges.binance.fetch_open_orders(symbol)
        sl_found = any(o['type'].upper() in ['STOP_MARKET', 'STOP'] for o in orders)
        tp_found = any(o['type'].upper() in ['TAKE_PROFIT_MARKET', 'LIMIT'] and o['side'].upper() != side for o in orders)
        
        print(f" >> SL Order: {'OK' if sl_found else 'MISSING'}")
        print(f" >> TP Order: {'OK' if tp_found else 'MISSING'}")
else:
    print("Binance not connected.")
