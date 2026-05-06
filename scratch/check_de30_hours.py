import MetaTrader5 as mt5
from datetime import datetime

if not mt5.initialize():
    print("MT5 INITIALIZATION FAILED")
    exit()

symbol = "DE30"
info = mt5.symbol_info(symbol)
if info:
    print(f"--- {symbol} INFO ---")
    print(f"Visible: {info.visible}")
    print(f"Trade Mode: {info.trade_mode}")
    
    # Check sessions
    # sessions are available via symbol_info but we need to check the specific day
    # MetaTrader5 doesn't provide a direct list of sessions via the python info object 
    # but we can check if it's currently tradeable.
    tick = mt5.symbol_info_tick(symbol)
    if tick:
        print(f"Last Tick: {datetime.fromtimestamp(tick.time)}")
        print(f"Bid/Ask: {tick.bid}/{tick.ask}")
    else:
        print("No tick data (Market likely closed)")

else:
    print(f"Symbol {symbol} not found")

mt5.shutdown()
