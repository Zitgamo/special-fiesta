from master import SovereignMaster
import MetaTrader5 as mt5

if __name__ == "__main__":
    if mt5.initialize():
        m = SovereignMaster()
        m.perform_market_scan()
        print(" >> SCAN COMPLETE. CHECK SQUADRON.JSON")
    else:
        print(" !! MT5 INIT FAILED")
