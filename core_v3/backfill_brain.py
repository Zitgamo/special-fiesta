import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = r"c:\Users\ADMIN\Desktop\IRON_COMMANDER_ELITE\core_v3\iron_core.db"

def backfill():
    print("="*60)
    print("SOVEREIGN BRAIN BACKFILL - Learning from History")
    print("="*60)
    
    if not os.path.exists(DB_PATH):
        print("DB not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Fetch closed trades from the last 14 days that have SL/TP info
    # We look for trades that have pnl and multipliers (or we estimate multipliers)
    query = """
        SELECT unit_id, symbol, side, sl, tp, price, pnl, sl_mult, tp_mult, er_at_entry
        FROM trades 
        WHERE (type = 'CLOSED' OR type = 'LIVE') AND pnl != 0
    """
    cursor.execute(query)
    trades = cursor.fetchall()
    
    print(f" Found {len(trades)} candidate trades for learning.")
    
    count = 0
    for t in trades:
        unit_id, symbol, side, sl, tp, entry_p, pnl, sl_m, tp_m, er = t
        
        # If multipliers are missing (legacy trades), we skip or estimate
        # For this backfill, let's only take trades that have the multipliers recorded
        if sl_m is None or tp_m is None:
            continue
            
        # Record to learning table
        cursor.execute("""
            INSERT INTO empirical_learning (unit_id, symbol, side, sl_mult, tp_mult, er_at_entry, outcome_pnl)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (unit_id, symbol, side, sl_m, tp_m, er or 0.5, pnl))
        count += 1
        
    conn.commit()
    conn.close()
    
    print(f" SUCCESS: Injected {count} experience samples into the Neural Net.")
    print("="*60)

if __name__ == "__main__":
    backfill()
