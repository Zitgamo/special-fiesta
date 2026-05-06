import sqlite3
import os

db_path = os.path.join("core_v3", "iron_core.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("SELECT symbol, volume, pnl FROM trades WHERE symbol LIKE '%JP225%'")
    rows = cursor.fetchall()
    print("--- JP225 TRADES ---")
    for row in rows:
        print(f"Symbol: {row[0]} | Volume: {row[1]} | PnL: {row[2]}")
except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()
