import MetaTrader5 as mt5
import time
import json
import os
import sys

# Add core_v3 to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from signal_commander import SignalCommander
from analytics import IronAnalytics

class PositionMonitor:
    def __init__(self):
        self.sc = SignalCommander()
        self.last_pnl_state = {} # symbol -> last_pnl
        self.trailing_notified = set() # symbol -> has_notified_trailing

    def run(self):
        # Load Real Secrets
        with open("core_v3/secrets_real.json", "r") as f:
            real_secrets = json.load(f)
            
        print(f" >> [CO-PILOT] Real-Monitor Active. Tracking Account: {real_secrets['login']}")
        
        # Initial Handshake
        if not mt5.initialize():
            print(" !! [FATAL] MT5 Init Failed.")
            return

        while True:
            try:
                # Only Login if not already logged in to the correct account
                acc_info = mt5.account_info()
                if not acc_info or acc_info.login != real_secrets['login']:
                    print(f" >> [AUTH] Synchronizing session for Account: {real_secrets['login']}...")
                    if not mt5.login(real_secrets['login'], password=real_secrets['password'], server=real_secrets['server']):
                        print(f" !! [AUTH_ERR] Failed to login: {mt5.last_error()}")
                        time.sleep(30)
                        continue
                
                # Load squadron for filtering
                try:
                    with open("core_v3/squadron.json", "r") as f:
                        squad = json.load(f)
                        elite_symbols = set(squad.get("ALPHA", []) + squad.get("OMEGA", []) + squad.get("GAMMA", []))
                except:
                    elite_symbols = set()

                positions = mt5.positions_get()
                if positions:
                    for pos in positions:
                        symbol = pos.symbol
                        
                        # FILTER: Only monitor Elite symbols or XAU (Stop Demo spam)
                        if symbol not in elite_symbols and "XAU" not in symbol:
                            continue

                        ticket = pos.ticket
                        pnl = pos.profit
                        entry = pos.price_open
                        current_price = pos.price_current
                        
                        # 1. PNL Heartbeat
                        last_pnl = self.last_pnl_state.get(symbol, 0)
                        if abs(pnl - last_pnl) > 5.0:
                            self.sc.send_alert("PROFIT UPDATE", symbol, f"Position {ticket} is active.", pnl=pnl)
                            self.last_pnl_state[symbol] = pnl

                        # 2. Trailing Stop Recommendation
                        atr = IronAnalytics.get_atr(symbol, None)
                        if atr and pnl > 0 and symbol not in self.trailing_notified:
                            price_dist = abs(current_price - entry)
                            if price_dist > (atr * 1.5):
                                self.sc.send_alert("🚀 TACTICAL ADVANCE", symbol, 
                                    f"Price has moved 1.5x ATR in your favor.\n\n"
                                    f"RECOMMENDATION: Move SL to BREAK-EVEN ({entry}) to lock in zero-risk.", pnl=pnl)
                                self.trailing_notified.add(symbol)

                # 3. Handle Closed Positions
                active_symbols = [p.symbol for p in (positions or [])]
                for sym in list(self.last_pnl_state.keys()):
                    if sym not in active_symbols:
                        self.sc.send_alert("STRIKE CONCLUDED", sym, "The position has been closed (SL, TP, or Manual). Check your history.")
                        del self.last_pnl_state[sym]
                        if sym in self.trailing_notified: self.trailing_notified.remove(sym)

                time.sleep(30)
            except Exception as e:
                print(f" !! [MONITOR_ERR] {e}")
                time.sleep(10)

if __name__ == "__main__":
    monitor = PositionMonitor()
    monitor.run()
