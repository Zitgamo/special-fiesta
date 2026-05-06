import MetaTrader5 as mt5
import sys
import os
sys.path.append("core_v3")
from vault_v2 import IronVault
from analytics import IronAnalytics

if not mt5.initialize():
    print("MT5 INITIALIZATION FAILED")
    exit()

vault = IronVault()
positions = mt5.positions_get()
if positions:
    print(f"--- REPAIRING SL/TP FOR {len(positions)} POSITIONS ---")
    for p in positions:
        if p.sl != 0 and p.tp != 0: continue # Skip if already has SL/TP
        
        symbol = p.symbol
        side = "BUY" if p.type == 0 else "SELL"
        price_open = p.price_open
        ticket = p.ticket
        
        # Calculate SL/TP
        atr = IronAnalytics.get_atr(symbol, None) # None for bridges, it will use MT5
        if not atr: atr = price_open * 0.001
        
        # Use GAMMA for JP225 as it's the harvester unit
        sl, tp = vault.get_sl_tp("GAMMA", symbol, side, price_open, atr)
        
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "sl": float(sl),
            "tp": float(tp)
        }
        
        result = mt5.order_send(request)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Ticket {ticket} | SL/TP SET: {sl}/{tp}")
        else:
            print(f"Ticket {ticket} | FAILED: {result.comment} (Code: {result.retcode})")
else:
    print("No positions found.")

mt5.shutdown()
