import MetaTrader5 as mt5

if not mt5.initialize():
    print("MT5 INITIALIZATION FAILED")
    exit()

all_pos = mt5.positions_get()
positions = [p for p in all_pos if "AUDUSD" in p.symbol.upper()]

if positions:
    print(f"--- CLOSING {len(positions)} AUDUSD POSITIONS (FOK MODE) ---")
    for p in positions:
        ticket = p.ticket
        symbol = p.symbol
        volume = p.volume
        side = p.type # 0 for BUY, 1 for SELL
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(volume),
            "type": mt5.ORDER_TYPE_SELL if side == 0 else mt5.ORDER_TYPE_BUY,
            "position": ticket,
            "price": mt5.symbol_info_tick(symbol).bid if side == 0 else mt5.symbol_info_tick(symbol).ask,
            "deviation": 20,
            "magic": 202605,
            "comment": "AUDUSD_PURGE",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }
        
        result = mt5.order_send(request)
        if result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Closed {ticket} | Result: DONE")
        else:
            print(f"Failed to close {ticket} | Error: {result.comment} (Code: {result.retcode})")
else:
    print("No AUDUSD positions found to close.")

mt5.shutdown()
