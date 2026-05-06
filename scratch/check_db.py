import sqlite3
import os

db_path = "core_v3/iron_core.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- TRADES SCHEMA ---")
cursor.execute("PRAGMA table_info(trades)")
for col in cursor.fetchall():
    print(col)

print("\n--- SAMPLE TRADES (last 5) ---")
cursor.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 5")
for row in cursor.fetchall():
    print(row)

conn.close()
