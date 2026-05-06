import MetaTrader5 as mt5

if not mt5.initialize():
    print("MT5 INITIALIZATION FAILED")
    exit()

positions = mt5.positions_get()
if positions:
    print(f"--- ACTIVE POSITIONS AUDIT ({len(positions)} total) ---")
    # Show first 10 for detailed check
    for p in positions[:10]:
        print(f"Ticket: {p.ticket} | Symbol: {p.symbol} | SL: {p.sl} | TP: {p.tp} | Magic: {p.magic}")
else:
    print("No active positions found.")

mt5.shutdown()
