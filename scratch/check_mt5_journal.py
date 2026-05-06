import MetaTrader5 as mt5
from datetime import datetime, timedelta

if not mt5.initialize():
    print("MT5 INITIALIZATION FAILED")
    exit()

print("--- MT5 TERMINAL STATUS ---")
term = mt5.terminal_info()
if term:
    print(f"Connected: {term.connected}")
    print(f"Trade Allowed: {term.trade_allowed}")
    print(f"Path: {term.path}")

print("\n--- RECENT MT5 ERRORS/JOURNAL ---")
# MT5 python API doesn't have a direct "read journal" function for the terminal log file.
# But we can check for recent execution errors.
last_error = mt5.last_error()
if last_error[0] != 1:
    print(f"Last Error: {last_error}")

# Check for failed orders in the history
print("\n--- FAILED ORDERS (Last 24h) ---")
from_date = datetime.now() - timedelta(days=1)
to_date = datetime.now()
history_orders = mt5.history_orders_get(from_date, to_date)
if history_orders:
    for order in history_orders:
        # Check for non-filled states
        if order.state not in [mt5.ORDER_STATE_FILLED, mt5.ORDER_STATE_PLACED]:
            print(f"Order {order.ticket} ({order.symbol}): State={order.state}, Comment={order.comment}")
else:
    print("No failed orders found in history.")

mt5.shutdown()
