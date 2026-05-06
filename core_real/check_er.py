from analytics import IronAnalytics
import MetaTrader5 as mt5

if __name__ == "__main__":
    if mt5.initialize():
        print(f"US30 ER: {IronAnalytics.get_efficiency_ratio('US30')}")
        print(f"XAUUSD ER: {IronAnalytics.get_efficiency_ratio('XAUUSD')}")
    else:
        print("MT5 INIT FAILED")
