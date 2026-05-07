import sqlite3
import os

DB_PATH = "iron_core.db"
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, symbol, side, pnl, timestamp FROM trades WHERE symbol = 'AUDUSD' ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    print("LAST 10 AUDUSD TRADES:")
    for r in rows:
        print(r)
    conn.close()
else:
    print("DB NOT FOUND")
