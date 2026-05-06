import MetaTrader5 as mt5

if not mt5.initialize():
    print("MT5 INITIALIZATION FAILED")
    exit()

print("--- PENDING ORDERS ---")
orders = mt5.orders_get()
if orders:
    for o in orders:
        if "AUDUSD" in o.symbol:
            print(f"Ticket: {o.ticket} | Symbol: {o.symbol} | Type: {o.type}")
else:
    print("No pending orders found.")

print("\n--- ACTIVE POSITIONS ---")
positions = mt5.positions_get()
if positions:
    for p in positions:
        if "AUDUSD" in p.symbol:
            print(f"Ticket: {p.ticket} | Symbol: {p.symbol} | Volume: {p.volume}")
else:
    print("No active positions found.")

mt5.shutdown()
