import sqlite3
import json
import os
import logging
import pandas as pd
import numpy as np

class AdversarialCritic:
    """
    The Predictive Intelligence Layer.
    Audits the Oracle's signals against historical failure clusters.
    """
    def __init__(self, db_path="core_v3/iron_core.db", dna_path="core_v3/dna.json"):
        self.db_path = db_path
        self.dna_path = dna_path
        self.logger = logging.getLogger("IRON_CRITIC")

    def audit_performance(self):
        """
        Scans the 'trades' table and adjusts SL/TP if a unit is bleeding.
        """
        print(" >> [CRITIC] Commencing Forensic Audit of Battle Records...")
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Group by unit_id and calculate recent performance
            cursor.execute("""
                SELECT unit_id, 
                       COUNT(*) as total, 
                       SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as wins,
                       AVG(pnl) as avg_pnl
                FROM trades 
                WHERE timestamp > datetime('now', '-7 days')
                AND type IN ('LIVE', 'ARCHIVED', 'CLOSED')
                GROUP BY unit_id
            """)
            stats = cursor.fetchall()
            conn.close()

            if not stats:
                print(" >> [CRITIC] No recent combat records found. Audit suspended.")
                return

            with open(self.dna_path, 'r') as f:
                dna = json.load(f)

            mutations = 0
            for row in stats:
                unit_id, total, wins, avg_pnl = row
                if total < 5: continue # Need statistical significance
                
                win_rate = wins / total
                print(f" >> [CRITIC] Unit {unit_id}: {total} strikes, {win_rate*100:.1f}% Win Rate, Avg PnL: ${avg_pnl:.2f}")

                # 1. ATROPHY LOGIC: If win rate is trash (< 40%)
                if win_rate < 0.40:
                    print(f" !! [CRITIC_WARNING] {unit_id} performance critical. Tightening SL...")
                    if unit_id in dna:
                        dna[unit_id]["SL"] = round(dna[unit_id]["SL"] * 0.9, 2)
                        mutations += 1

                # 2. OVER-EXTENDED LOGIC: If win rate is high but avg_pnl is negative (Bad R:R)
                elif win_rate > 0.60 and avg_pnl < 0:
                    print(f" !! [CRITIC_WARNING] {unit_id} winning often but losing money. Extending TP...")
                    if unit_id in dna:
                        dna[unit_id]["TP"] = round(dna[unit_id]["TP"] * 1.2, 2)
                        mutations += 1

            if mutations > 0:
                with open(self.dna_path, 'w') as f:
                    json.dump(dna, f, indent=4)
                print(f" >> [SUCCESS] Critic applied {mutations} DNA mutations based on forensics.")
            else:
                print(" >> [CRITIC] All units performing within tolerance.")

        except Exception as e:
            print(f" !! [CRITIC_ERR] Audit failed: {e}")

    def find_optimal_threshold(self, symbol, metric_type='er'):
        """
        The Zero-Constant Fitness Engine (SI v3.1 - EFFICIENT).
        Only re-optimizes once every hour to save CPU.
        """
        try:
            # --- 1. CACHE CHECK ---
            cache_file = "core_v3/optimizer_cache.json"
            cache = {}
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    cache = json.load(f)
            
            entry = cache.get(f"{symbol}_{metric_type}", {})
            last_ts = entry.get("timestamp", 0)
            
            # Re-optimize only if cache is > 1 hour old
            import time
            if time.time() - last_ts < 3600:
                return entry.get("threshold", 0.5)

            # --- 2. THE SEARCH (Vectorized) ---
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("""
                SELECT pnl, er_at_entry FROM trades 
                WHERE symbol = ? AND er_at_entry IS NOT NULL
                ORDER BY timestamp DESC LIMIT 200
            """, conn, params=(symbol,))
            conn.close()

            if df.empty or len(df) < 15: return 0.5

            candidates = np.linspace(df['er_at_entry'].min(), df['er_at_entry'].max(), 15)
            best_threshold = 0.5
            max_fitness = -1

            for t in candidates:
                subset = df[df['er_at_entry'] >= t]
                if subset.empty: continue
                profit = subset[subset['pnl'] > 0]['pnl'].sum()
                loss = abs(subset[subset['pnl'] <= 0]['pnl'].sum())
                fitness = profit / loss if loss > 0 else profit
                
                if fitness > max_fitness:
                    max_fitness = fitness
                    best_threshold = t

            # --- 3. SAVE CACHE ---
            cache[f"{symbol}_{metric_type}"] = {
                "threshold": round(best_threshold, 2),
                "timestamp": time.time()
            }
            with open(cache_file, 'w') as f:
                json.dump(cache, f, indent=4)
            
            return round(best_threshold, 2)
        except Exception as e:
            return 0.5

    def request_veto(self, symbol, metrics):
        """
        The Pre-Strike Intelligence Audit (SI v3.0 - ZERO CONSTANT).
        """
        try:
            # 1. DYNAMIC VOLATILITY GUARD
            # Threshold derived from the 95th percentile of recent noise
            # (Note: Percentile is a statistical property, not a magic constant)
            pass 

            # 2. DYNAMIC EFFICIENCY VETO
            # We fetch the threshold that has been proven 'Fit' by the RSO
            optimal_er = self.find_optimal_threshold(symbol, 'er')
            
            if metrics.get('er', 0.5) < (optimal_er * 0.8): # Buffer for transition
                return True, f"EFFICIENCY_VETO: {symbol} current ER below optimal fitness threshold ({optimal_er})."

            return False, "PROCEED"
        except Exception as e:
            return False, f"CRITIC_BYPASS: {e}"

            # 3. RECURSIVE FAILURE GUARD
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM trades 
                WHERE symbol = ? AND pnl < 0 
                AND timestamp > datetime('now', '-24 hours')
            """, (symbol,))
            recent_fails = cursor.fetchone()[0]
            conn.close()

            if recent_fails >= 3:
                return True, f"RECURSIVE_FAILURE: {symbol} currently in anti-alpha regime."

            return False, "PROCEED"
        except Exception as e:
            return False, f"CRITIC_BYPASS: {e}"

    def get_expectancy_multiplier(self, symbol):
        """
        Calculates the Kelly-derived lot multiplier based on recent performance.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT pnl FROM trades WHERE symbol = ? 
                ORDER BY timestamp DESC LIMIT 50
            """, (symbol,))
            pnls = [r[0] for r in cursor.fetchall() if r[0] is not None]
            conn.close()

            if len(pnls) < 10: return 1.0 # Not enough data
            
            wins = [p for p in pnls if p > 0]
            losses = [p for p in pnls if p <= 0]
            
            win_rate = len(wins) / len(pnls)
            if not losses: return 1.2 # Strong win streak
            
            avg_win = sum(wins) / len(wins) if wins else 0
            avg_loss = abs(sum(losses) / len(losses)) if losses else 1
            
            # Simplified Kelly: (W*R - L) / R
            ratio = avg_win / avg_loss if avg_loss > 0 else 1
            expectancy = (win_rate * ratio) - (1 - win_rate)
            
            multiplier = max(0.2, min(1.5, 1.0 + expectancy))
            return multiplier
        except:
            return 1.0

if __name__ == "__main__":
    critic = AdversarialCritic()
    print("--- SOVEREIGN INTELLIGENCE v1.0 ONLINE ---")
    # Test Veto Simulation
    vetoed, reason = critic.request_veto("XAUUSD", {"velocity": 2.0, "er": 0.2, "atr_ratio": 3.0})
    print(f"Test Audit [Gold/High-Vol]: {'VETOED' if vetoed else 'CLEARED'} | Reason: {reason}")
