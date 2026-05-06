import MetaTrader5 as mt5
import os

def check():
    if not mt5.initialize():
        print("MT5 Init Failed")
        return

    symbol = "JP225"
    info = mt5.symbol_info(symbol)
    if info:
        print(f"Symbol: {symbol}")
        print(f"Volume Min: {info.volume_min}")
        print(f"Volume Max: {info.volume_max}")
        print(f"Volume Step: {info.volume_step}")
        print(f"Contract Size: {info.trade_contract_size}")
    else:
        print(f"Symbol {symbol} not found")
    
    mt5.shutdown()

if __name__ == "__main__":
    check()
