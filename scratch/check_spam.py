import sqlite3
import os

db_path = "core_v3/iron_core.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT symbol, unit_id, timestamp, pnl FROM trades WHERE exit_price IS NULL ORDER BY timestamp DESC LIMIT 50;")
    rows = cursor.fetchall()
    print("SYMBOL | UNIT | TIMESTAMP | PNL")
    print("-" * 50)
    for r in rows:
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")
    conn.close()
else:
    print(f"Database not found at {db_path}")
