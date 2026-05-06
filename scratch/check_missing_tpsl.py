import MetaTrader5 as mt5

if not mt5.initialize():
    print("MT5 INITIALIZATION FAILED")
    exit()

positions = mt5.positions_get()
if positions:
    missing = [p for p in positions if p.sl == 0 or p.tp == 0]
    print(f"--- POSITIONS MISSING SL/TP ({len(missing)} out of {len(positions)}) ---")
    for p in missing:
        print(f"Ticket: {p.ticket} | Symbol: {p.symbol} | SL: {p.sl} | TP: {p.tp}")
else:
    print("No active positions found.")

mt5.shutdown()
