import sqlite3
import os

db_path = "core_v3/iron_core.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Select open trades (exit_price is NULL)
    cursor.execute("SELECT symbol, price, sl, tp, pnl, unit_id FROM trades WHERE symbol IN ('DE30', 'US30', 'GER40') AND exit_price IS NULL ORDER BY price ASC;")
    rows = cursor.fetchall()
    print("SYMBOL | ENTRY | SL | TP | PNL | UNIT")
    print("-" * 50)
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}")
    conn.close()
else:
    print(f"Database not found at {db_path}")
