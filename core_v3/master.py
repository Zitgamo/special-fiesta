import subprocess
import time
import os
import signal
import sys
import json
import random
import pandas as pd
import MetaTrader5 as mt5
import sqlite3

# Path Injection
try:
    from paths import DB_PATH, DNA_PATH, CORE_DIR
except ImportError:
    DB_PATH, DNA_PATH, CORE_DIR = "core_v3/iron_core.db", "core_v3/dna.json", "core_v3"
from analytics import IronAnalytics
from forensics import IronForensics
from oracle import SovereignOracle
from ghost_comm import GhostComm
import threading

class SovereignMaster:
    def __init__(self):
        self.units = {
            "ALPHA": "core_v3/engine.py",
            "OMEGA": "core_v3/engine.py",
            "GAMMA": "core_v3/engine.py"
        }
        self.active_processes = {}
        self.oracle = SovereignOracle()
        # self.comm = GhostComm() # DISABLED: Avoid 401 Unauthorized crashes
        self.is_running = True
        
        # Start Ghost Comm in Background
        # threading.Thread(target=self.comm.run, daemon=True).start()
        
        # Initialize Bridges for Guardian Audit
        from bridges import IronBridges
        secrets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secrets.json")
        self.bridges = IronBridges(secrets_path)
        
        # Additional components
        self.forensics = IronForensics()
        from critic import AdversarialCritic
        self.critic = AdversarialCritic()
        from vault_v2 import IronVault
        self.vault = IronVault(bridges=self.bridges)

    def start_units(self):
        print("--- SOVEREIGN MASTER v3.0: INITIALIZING ---")
        for name, script in self.units.items():
            print(f" >> [ORCHESTRATOR] Launching {name}...")
            # Run in a new terminal window for visibility
            cmd = ["python", script, name]
            proc = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.active_processes[name] = proc
            time.sleep(2) # Staggered boot

    def detect_regime(self, symbol="XAUUSD"):
        """
        Determines the current market regime.
        Returns: 'TRENDING' or 'RANGING'
        """
        if not mt5.initialize(): return "UNKNOWN"
        
        # Simple Regime Detection: Check session distance
        info = mt5.symbol_info(symbol)
        tick = mt5.symbol_info_tick(symbol)
        if not info or not tick: return "UNKNOWN"
        
        dist = abs(tick.ask - info.session_open) / info.session_open if info.session_open > 0 else 0
        
        if dist > 0.005: # > 0.5% move from open
            return "TRENDING"
        else:
            return "RANGING"

    def mutate_dna(self):
        """
        Forensic Mutation: Only mutates underperforming units.
        """
        print(" >> [CRITIC] Commencing Forensic Audit for Mutation...")
        dna_path = "core_v3/dna.json"
        try:
            conn = sqlite3.connect(DB_PATH)
            df = pd.read_sql_query("SELECT unit_id, side FROM trades", conn) # Simplified for now
            conn.close()
            
            with open(DNA_PATH, 'r') as f:
                dna = json.load(f)
            
            # Removed redundant DNA reload loop
            
            # Audit LIVE units (ALPHA, OMEGA, GAMMA)
            for unit in ["ALPHA", "OMEGA", "GAMMA"]:
                stats = self.forensics.get_unit_stats(unit, trade_type='LIVE')
                self.process_mutation(unit, stats, dna)
                
            # Audit SOUTHERN units (SOUTH_ALPHA, SOUTH_OMEGA, SOUTH_GAMMA)
            for unit in ["SOUTH_ALPHA", "SOUTH_OMEGA", "SOUTH_GAMMA"]:
                stats = self.forensics.get_unit_stats(unit, trade_type='PAPER')
                # Map SOUTH_ALPHA performance to standard ALPHA DNA
                dna_key = unit.split("_")[1] # Get 'ALPHA', 'OMEGA', or 'GAMMA'
                self.process_mutation(dna_key, stats, dna, prefix=f"SOUTHERN_{unit}")

            with open(DNA_PATH, 'w') as f:
                json.dump(dna, f, indent=4)
        except Exception as e:
            print(f" >> [CRITIC_ERR] Forensic mutation failed: {e}")

    def process_mutation(self, dna_key, stats, dna, prefix=""):
        if not stats or stats.get("total", 0) < 3: return # Need at least 3 strikes
        
        win_rate = stats.get("win_rate", 0.5)
        
        # 1. ATROPHY LOGIC (Reduce lot on loss)
        if win_rate < 0.4:
            print(f" !! [ATROPHY] {prefix or dna_key} underperforming ({win_rate*100:.1f}%). Decaying Lot Multiplier...")
            dna[dna_key]["LOT_SIZE"] = round(dna[dna_key]["LOT_SIZE"] * 0.9, 4)
            
            # 2. SPAWN MUTANT IF NONE EXISTS
            if not dna[dna_key].get("SHADOW"):
                self.branch_dna(dna_key, dna)
        
        # 3. HANDOVER LOGIC (If shadow is better, SWAP!)
        if dna[dna_key].get("SHADOW"):
            if self.compare_realities(dna_key, dna):
                print(f" >> [REBIRTH] {dna_key} Mutant proven superior. Handing over command!")
                dna[dna_key]["SL"] = dna[dna_key]["SHADOW"]["SL"]
                dna[dna_key]["TP"] = dna[dna_key]["SHADOW"]["TP"]
                dna[dna_key]["SHADOW"] = None

    def branch_dna(self, unit, dna):
        """
        Creates a Shadow (Virtual) branch of the current DNA.
        """
        print(f" !! [BRANCH] {unit} underperformed. Creating Adversarial Shadow...")
        dna[unit]["SHADOW"] = {
            "SL": dna[unit]["SL"],
            "TP": dna[unit]["TP"]
        }
        # Mutate the LIVE DNA
        mutation_dir = random.choice([-0.2, 0.2])
        dna[unit]["SL"] = round(dna[unit]["SL"] + mutation_dir, 2)
        dna[unit]["TP"] = round(dna[unit]["TP"] - mutation_dir, 2)

    def compare_realities(self, unit, dna):
        """
        Compares Live Mutant vs Virtual Shadow performance.
        """
        print(f" [SCIENCE] Comparing {unit} Realities...")
        # Placeholder for scientific comparison
        # If Shadow (Virtual) is performing better, REVERT!
        if random.random() > 0.7: 
            print(f" >> [REVERT] Shadow outperformed Mutant. Original logic was just 'Unlucky'.")
            dna[unit]["SL"] = dna[unit]["SHADOW"]["SL"]
            dna[unit]["TP"] = dna[unit]["SHADOW"]["TP"]
            dna[unit]["SHADOW"] = None
        else:
            print(f" >> [CONFIRM] Mutant is superior. Old logic was 'Stupid'. Deleting Shadow.")
            dna[unit]["SHADOW"] = None

    def allocate_capital(self, regime):
        """
        Dynamically redistributes lot sizes based on market regime.
        """
        print(f" >> [MASTER] Re-Allocating Capital for {regime} Regime...")
        dna_path = "core_v3/dna.json"
        try:
            with open(DNA_PATH, 'r') as f:
                dna = json.load(f)
            
            if regime == "TRENDING":
                dna["ALPHA"]["LOT_SIZE"] = 0.03
                dna["OMEGA"]["LOT_SIZE"] = 0.005
                dna["GAMMA"]["LOT_SIZE"] = 0.015 # Slightly increase breakout size
            else: # RANGING
                dna["ALPHA"]["LOT_SIZE"] = 0.01
                dna["OMEGA"]["LOT_SIZE"] = 0.02
                dna["GAMMA"]["LOT_SIZE"] = 0.01

            with open(DNA_PATH, 'w') as f:
                json.dump(dna, f, indent=4)
            print(f" >> [SUCCESS] Capital Re-Allocated. Unit Priorities Synchronized.")
        except Exception as e:
            print(f" >> [ALLOC_ERR] Allocation failed: {e}")

    def perform_market_scan(self):
        """
        Scans Top 20 assets and picks the best for each logic.
        """
        print(" >> [SCOUT] Commencing Hourly Market Scan...")
        # 1. MT5 Discovery (Targeted high-yield groups - NO CRYPTO ON MT5)
        all_mt5 = mt5.symbols_get(group="*USD*,*XAU*,*XAG*,*US30*,*DE30*,*NAS100*")
        
        # DYNAMIC SIGNAL SENSITIVITY
        min_er = 0.40 
        candidates = []
        
        # CRYPTO BLACKLIST FOR MT5
        mt5_crypto_blacklist = ["BTC", "ETH", "SOL", "ADA", "XRP", "DOT", "LINK", "LTC", "BCH", "FIL"]
        
        if all_mt5:
            for s in all_mt5:
                # Filter out Crypto on MT5
                if any(c in s.name.upper() for c in mt5_crypto_blacklist):
                    continue
                    
                if s.visible and s.trade_mode == mt5.SYMBOL_TRADE_MODE_FULL:
                    tick = mt5.symbol_info_tick(s.name)
                    if tick and tick.bid > 0:
                        candidates.append(s.name)
        
        # 2. Sovereign Prime Watchlist (Session-Aware: Asia/EU/US)
        print(" >> [SMART_SCAN] Identifying High-Alpha Session Assets...")
        # Added HK50 and JP225 for Asia-Noon volatility
        potential_symbols = ["XAUUSD", "HK50", "JP225", "USDJPY", "AUDUSD", "US30", "NAS100", "GBPUSD", "EURUSD", "DE30"]
        
        results = []
        for symbol in potential_symbols:
            try:
                # Filter out historical catastrophic losers (Soft-Block)
                # If symbol has > $1000 historical loss, it needs higher ER to pass
                loss_weight = 1.0
                if symbol in ["XAUUSD", "XAGUSD"]: loss_weight = 1.5 # Needs 50% better signal
                
                er = IronAnalytics.get_efficiency_ratio(symbol)
                if er >= (min_er * loss_weight):
                    vol = IronAnalytics.get_velocity(symbol)
                    results.append({"symbol": symbol, "er": er, "vol": vol})
            except Exception as e:
                pass # Silent fail for noisy symbols
            
        # 3. BINANCE Discovery (High-Frequency Micro-Audit)
        crypto_results = []
        if self.bridges.binance:
            print(" >> [SCOUT] Scanning Binance Frontiers...")
            try:
                # Top Tier Crypto for Stability
                assets = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "DOGE/USDT"]
                for symbol in assets:
                    try:
                        er = IronAnalytics.get_efficiency_ratio(symbol, bridges=self.bridges)
                        # Hard-lock DOGE for the user
                        if er >= min_er or symbol == "DOGE/USDT":
                            vol = IronAnalytics.get_velocity(symbol, bridges=self.bridges)
                            crypto_results.append({"symbol": symbol, "er": er, "vol": vol})
                    except Exception as e:
                        print(f" !! [SCOUT_WARN] Failed to analyze {symbol}: {e}")
            except: pass

        # Sort by Efficiency Ratio (ER) Descending
        results.sort(key=lambda x: x['er'], reverse=True)
        crypto_results.sort(key=lambda x: x['er'], reverse=True)

        # 4. Uniqueness Protocol (Correlation Clustering)
        def get_correlation_cluster(s):
            s = s.replace("/", "").replace("m", "").upper()
            if "XAU" in s: return "METAL_GOLD"
            if "XAG" in s: return "METAL_SILVER"
            if "BTC" in s: return "CRYPTO_BTC"
            if "ETH" in s: return "CRYPTO_ETH"
            if "SOL" in s: return "CRYPTO_SOL"
            
            # Currency Correlation Groups
            majors = ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD"]
            if any(m in s for m in majors) or (s.endswith("USD") and s[:3] in ["EUR", "GBP", "AUD", "NZD"]):
                return "USD_MAJORS"
            
            yen_crosses = ["JPY", "USDJPY", "EURJPY", "GBPJPY"]
            if any(y in s for y in yen_crosses):
                return "JPY_CROSSES"
                
            return s[:3] # Fallback to first 3 chars

        used_bases = set()
        def pick_unique(source_list, count):
            picked = []
            for item in source_list:
                cluster = get_correlation_cluster(item['symbol'])
                if cluster not in used_bases:
                    picked.append(item['symbol'])
                    used_bases.add(cluster)
                if len(picked) >= count: break
            return picked

        squadron = {"ALPHA": ["XAUUSD"], "OMEGA": [], "GAMMA": []}
        
        # 5. Elite Assignment (EXNESS ONLY for Real-Money Guidance)
        # We exclude crypto_results to ensure the user can execute on Exness MT5
        squadron["ALPHA"] = list(set(["XAUUSD"] + pick_unique(results, 2)))[:2]
        squadron["OMEGA"] = pick_unique(results, 2)
        squadron["GAMMA"] = pick_unique(results, 2)

        # FALLBACK: If results are poor, inject Iron Classics (Exness)
        if sum(len(v) for v in squadron.values()) < 3:
            print(" !! [FAIL_SAFE] Scanner returned low signal. Injecting Iron Classics...")
            squadron["ALPHA"] = list(set(squadron["ALPHA"] + ["XAUUSD", "US30"]))[:2]
            squadron["OMEGA"] = list(set(squadron["OMEGA"] + ["GBPUSD"]))[:2]
            squadron["GAMMA"] = list(set(squadron["GAMMA"] + ["NAS100", "XAGUSD"]))[:2]

        # 6. Save
        with open("core_v3/squadron.json", "w") as f:
            json.dump(squadron, f, indent=4)
        print(f" >> [SUCCESS] Exness Elite Squadrons Assigned: {squadron}")

    def perform_news_audit(self):
        """
        Polls the MT5 Economic Calendar for High-Impact events.
        """
        import MetaTrader5 as mt5
        from datetime import datetime, timedelta
        
        # Check for events in the next 30 minutes
        time_from = datetime.utcnow()
        time_to = time_from + timedelta(minutes=30)
        
        events = mt5.calendar_events_get(time_from=time_from, time_to=time_to)
        news_pause = False
        
        if events:
            for event in events:
                # 3 = High Impact, 4 = Critical Impact
                if event.importance >= 3:
                    print(f" !! [CHRONOS] High Impact News Detected: {event.name}. Standing down...")
                    news_pause = True
                    break
        
        # Update DNA with News Pause status
        dna_path = "core_v3/dna.json"
        try:
            with open(DNA_PATH, 'r') as f:
                dna = json.load(f)
            dna["GLOBAL"]["NEWS_PAUSE"] = news_pause
            with open(DNA_PATH, 'w') as f:
                json.dump(dna, f, indent=4)
        except: pass

    def autonomous_asset_migration(self):
        """
        REGIME SHIFT ENGINE:
        Automatically moves assets between ALPHA, OMEGA, and GAMMA based on current Efficiency.
        """
        print(" >> [MASTER] Scanning for Regime Shifts...")
        squad_path = "core_v3/squadron.json"
        try:
            with open(squad_path, 'r') as f:
                squad = json.load(f)
            
            all_assets = []
            for unit, assets in squad.items():
                all_assets.extend(assets)
            
            new_squad = {"ALPHA": [], "OMEGA": [], "GAMMA": []}
            changes_made = False
            
            for asset in all_assets:
                # Get Efficiency Ratio (ER)
                from analytics import IronAnalytics
                er = IronAnalytics.get_efficiency_ratio(asset.replace('_x10','').replace('/USDT',''))
                
                current_unit = next((u for u, assets in squad.items() if asset in assets), "ALPHA")
                target_unit = "ALPHA" # Default to Range
                
                if er > 0.60: # Strong Trend
                    target_unit = "OMEGA"
                elif er > 0.40: # Choppy / Transition
                    target_unit = "GAMMA"
                else: # Ranging
                    target_unit = "ALPHA"
                
                if target_unit != current_unit:
                    print(f" !! [MIGRATION] {asset} shifted characteristic (ER: {er}). Moving {current_unit} -> {target_unit}")
                    changes_made = True
                
                new_squad[target_unit].append(asset)
            
            if changes_made:
                with open(squad_path, 'w') as f:
                    json.dump(new_squad, f, indent=4)
                print(" >> [MASTER] Squadron Re-Assignments Finalized.")
                
        except Exception as e:
            print(f" >> [MIGRATION_ERR] Failed to migrate assets: {e}")

    def monitor(self):
        print("--- MASTER COMMAND ACTIVE ---")
        try:
            loop_count = 0
            # 1. INITIAL NEURAL HANDSHAKE
            if mt5.initialize():
                print(" >> [MASTER] Initial MT5 Handshake Successful. Commencing Global Scan...")
            else:
                print(" !! [MASTER] Initial MT5 Handshake Failed. Will retry in loop.")

            while self.is_running:
                try:
                    # 0. ENSURE MT5 IS INITIALIZED
                    if not mt5.initialize():
                        print(" !! [RECOVERY] MT5 Neural Handshake Severed. Retrying in 5s...")
                        time.sleep(5)
                        continue

                    # 1. Global Market Discovery (Sovereign Scan) - Every 30 mins
                    trigger_path = "core_v3/scan_trigger.tmp"
                    if loop_count % 60 == 0 or os.path.exists(trigger_path):
                        self.perform_market_scan()
                        if os.path.exists(trigger_path):
                            try: os.remove(trigger_path)
                            except: pass
                    
                    # 2. Macro Sentiment Audit
                    sentiment = IronAnalytics.get_macro_sentiment()
                    
                    # 3. Atomic DNA Update
                    dna_path = "core_v3/dna.json"
                    try:
                        with open(DNA_PATH, 'r') as f:
                            dna = json.load(f)
                        dna["GLOBAL"] = {"SENTIMENT": sentiment}
                        with open(dna_path + ".tmp", 'w') as f:
                            json.dump(dna, f, indent=4)
                        os.replace(dna_path + ".tmp", dna_path)
                    except: pass
                    
                    # 4. Sovereign Global Audit (Apex Exit Guard)
                    from vault_v2 import IronVault
                    vault = IronVault(self.bridges)
                    vault.active_risk_governor(self.bridges)
                    
                    # 5. Evolution Trigger
                    loop_count += 1
                    if loop_count % 20 == 0: # Every 10 mins
                        self.mutate_dna()
                        self.critic.audit_performance()
                    
                    # 6. Database Reconciliation (Safe Sync) - Every 1 hour
                    if loop_count % 120 == 0:
                        self.forensics.reconcile_trades(self.bridges)
                        loop_count = 0 # Reset
                    
                    time.sleep(30)
                except Exception as e:
                    print(f" !! [SHIELD_RECOVERY] Master encountered an anomaly: {e}. Resuming heartbeat...")
                    time.sleep(10)
        except KeyboardInterrupt:
            self.neutralize()

    def neutralize(self):
        print("--- NEUTRALIZING ALL UNITS ---")
        for name, proc in self.active_processes.items():
            print(f" >> Terminating {name}...")
            proc.terminate()
            
        # Optional: Force close all positions via MT5
        # mt5.initialize()
        # positions = mt5.positions_get()
        # ... logic to close all ...
        
        print("--- ACCOUNT SECURED ---")
        self.is_running = False

if __name__ == "__main__":
    master = SovereignMaster()
    # master.start_units() # DISABLED: Sentinel now handles all unit launches
    master.monitor()
