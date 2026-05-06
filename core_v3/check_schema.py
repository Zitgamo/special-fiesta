import sqlite3
import os

DB_PATH = "iron_core.db"
if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(trades)")
    cols = cursor.fetchall()
    print("TRADES TABLE COLS:")
    for c in cols:
        print(c)
    conn.close()
else:
    print("DB NOT FOUND")
