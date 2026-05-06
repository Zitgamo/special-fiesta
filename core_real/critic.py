import sqlite3
import json
import os
import logging

class AdversarialCritic:
    """
    The Forensic Auditor.
    Analyzes historical performance and suggests DNA mutations to the Master.
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
                        # Tighten SL by 10%
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

if __name__ == "__main__":
    critic = AdversarialCritic()
    critic.audit_performance()
