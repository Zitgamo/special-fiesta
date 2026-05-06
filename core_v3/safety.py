import time
import logging
import os
import json
import psutil
import MetaTrader5 as mt5
import sqlite3

# Path Injection
try:
    from paths import DB_PATH
except ImportError:
    DB_PATH = "core_v3/iron_core.db"

class IronSafety:
    def __init__(self, db_path=None):
        self.logger = logging.getLogger("IRON_SAFETY")
        self.MAX_TOTAL_LOTS = 0.20 # Absolute fleet-wide cap
        self.MAX_UNIT_LOTS = 0.05  # Per-unit cap
        self.MAX_STRIKES_PER_HOUR = 3
        self.MAX_SPREAD_ATR_RATIO = 0.20 # If spread > 20% of ATR, abort
        self.db_path = db_path
        
        # Persistent memory for circuit breakers
        self.last_strikes = [] # List of timestamps

    def pre_flight_audit(self, unit_id, symbol, side, lot, price, atr, spread):
        """
        The Forensic Filter. Returns (Allowed: bool, Reason: str)
        """
        # 1. MATHEMATICAL SANITY (The Burn Bug Guard)
        if lot > self.MAX_UNIT_LOTS:
            return False, f"LOT_SIZE_OVER_CAP ({lot} > {self.MAX_UNIT_LOTS})"
            
        if lot <= 0:
            return False, "INVALID_LOT_SIZE_ZERO"

        # 2. VOLATILITY SANITY (The News/Spread Guard)
        if atr <= 0:
            return False, "ATR_DATA_STALE_OR_ZERO"
            
        if spread > (atr * self.MAX_SPREAD_ATR_RATIO):
            return False, f"SPREAD_TOO_HIGH ({spread} > {atr * self.MAX_SPREAD_ATR_RATIO})"

        # 3. TEMPORAL SANITY (The Global Loop Attack Guard)
        strike_log_path = "core_v3/strike_frequency.json"
        symbol_log_path = "core_v3/symbol_cooldown.json"
        now = time.time()
        
        # --- SYMBOL COOLDOWN (Task 11: Anti-Spam) ---
        symbol_tracker = {}
        if os.path.exists(symbol_log_path):
            try:
                with open(symbol_log_path, 'r') as f:
                    symbol_tracker = json.load(f)
            except: pass
            
        last_strike = symbol_tracker.get(symbol, 0)
        if now - last_strike < 1800: # 30 Minute Cooldown per symbol
            return False, f"SYMBOL_COOLDOWN_ACTIVE ({int(1800 - (now - last_strike))}s remaining)"

        # --- GLOBAL FREQUENCY (Task 11: Race Condition Guard) ---
        # Retry logic for reading/writing global strike log
        passed_global = False
        for attempt in range(5):
            try:
                strikes = []
                if os.path.exists(strike_log_path):
                    with open(strike_log_path, 'r') as f:
                        strikes = json.load(f)
                
                strikes = [t for t in strikes if now - t < 3600]
                if len(strikes) >= self.MAX_STRIKES_PER_HOUR:
                    return False, f"GLOBAL_FREQUENCY_LIMIT ({len(strikes)}/hr)"
                
                # If we reach here, we pass global check. Log it!
                strikes.append(now)
                with open(strike_log_path, 'w') as f:
                    json.dump(strikes, f)
                passed_global = True
                break # Success
            except:
                time.sleep(0.1) # Backoff
        
        if not passed_global:
            return False, "SAFETY_LOCK_BUSY"

        # 4. PRICE VALIDITY (Flash Crash Guard)
        if price <= 0:
            return False, "PRICE_DATA_CORRUPT"

        # Update symbol tracker
        symbol_tracker[symbol] = now
        try:
            with open(symbol_log_path, 'w') as f:
                json.dump(symbol_tracker, f)
        except: pass
        
        self.logger.info(f" !! [SAFETY_PASS] {unit_id} validated for {symbol} {side} {lot}")
        return True, "SAFE"

    def global_exposure_audit(self, active_positions):
        """
        Ensures the entire fleet doesn't over-leverage the mother ship.
        """
        total_lots = sum(float(p.get('volume', 0)) for p in active_positions)
        if total_lots >= self.MAX_TOTAL_LOTS:
            return False, f"GLOBAL_EXPOSURE_LIMIT_REACHED ({total_lots})"
        return True, "SAFE"

    def system_integrity_audit(self):
        """
        FAIL-CLOSED ARCHITECTURE (v3.0):
        The Dead Man's Switch. If the Master is dead, the fleet must halt.
        """
        # 1. Master Process Check
        master_alive = False
        try:
            for p in psutil.process_iter(['cmdline']):
                if p.info['cmdline'] and any("master.py" in s.lower() for s in p.info['cmdline']):
                    master_alive = True
                    break
        except: pass
        
        if not master_alive:
            return False, "MASTER_OFFLINE_FAIL_CLOSED"

        # 2. Database "Kill Switch" Check
        try:
            conn = sqlite3.connect(self.db_path or DB_PATH)
            cursor = conn.cursor()
            # Check for a global pause flag if it exists
            cursor.execute("SELECT value FROM hq_config WHERE key = 'GLOBAL_PAUSE'")
            res = cursor.fetchone()
            if res and res[0] == '1':
                return False, "GLOBAL_PAUSE_ACTIVE"
            conn.close()
        except: pass

        return True, "SYSTEM_HEALTHY"
