import sqlite3
import os

db_path = "core_v3/iron_core.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, price, pnl, unit_id, timestamp, status FROM trades ORDER BY timestamp DESC LIMIT 20;")
    rows = cursor.fetchall()
    print("SYMBOL | ENTRY | PNL | UNIT | TIME | STATUS")
    print("-" * 70)
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]}")
    conn.close()
else:
    print(f"Database not found at {db_path}")
