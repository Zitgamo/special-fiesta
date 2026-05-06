import sqlite3
import os

db_path = "core_v3/iron_core.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Select last 10 closed trades (exit_price is NOT NULL)
    cursor.execute("SELECT symbol, price, exit_price, pnl, unit_id, timestamp FROM trades WHERE exit_price IS NOT NULL ORDER BY timestamp DESC LIMIT 10;")
    rows = cursor.fetchall()
    print("SYMBOL | ENTRY | EXIT | PNL | UNIT | TIME")
    print("-" * 60)
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}")
    conn.close()
else:
    print(f"Database not found at {db_path}")
