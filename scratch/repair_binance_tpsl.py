import sys
import os
sys.path.append("core_v3")
from bridges import IronBridges
from vault_v2 import IronVault
from analytics import IronAnalytics

secrets_path = "core_v3/secrets.json"
bridges = IronBridges(secrets_path)
vault = IronVault(bridges=bridges)

if bridges.binance:
    print("--- BINANCE SL/TP REPAIR (FINAL) ---")
    positions = bridges.binance.fetch_positions()
    for p in positions:
        vol = float(p['contracts'])
        if vol == 0: continue
        
        symbol = p['symbol'].split(':')[0]
        side = p['side'].upper()
        price_open = float(p['entryPrice'])
        
        # Check open orders
        orders = bridges.binance.fetch_open_orders(symbol)
        sl_found = any(o['type'].upper() in ['STOP_MARKET', 'STOP'] for o in orders)
        
        if not sl_found:
            print(f"Repairing SL for {symbol} ({side})...")
            atr = IronAnalytics.get_atr(symbol, bridges)
            if not atr: atr = price_open * 0.001
            
            vault_side = "BUY" if side == "LONG" else "SELL"
            sl, tp = vault.get_sl_tp("OMEGA", symbol, vault_side, price_open, atr)
            
            try:
                params = {
                    'stopPrice': sl,
                    'type': 'STOP_MARKET',
                    'positionSide': side
                }
                order_side = 'SELL' if side == 'LONG' else 'BUY'
                res = bridges.binance.create_order(symbol, 'STOP_MARKET', order_side, abs(vol), params=params)
                print(f" >> SL Created @ {sl} | Result: {res['id']}")
            except Exception as e:
                print(f" >> FAILED to create SL: {e}")
else:
    print("Binance not connected.")
