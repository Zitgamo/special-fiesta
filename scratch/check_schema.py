import sqlite3
import os

db_path = "core_v3/iron_core.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(trades);")
    cols = cursor.fetchall()
    for c in cols:
        print(c)
    conn.close()
