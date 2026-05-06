import sqlite3
import os

DB_PATH = r"c:\Users\ADMIN\Desktop\IRON_COMMANDER_ELITE\core_v3\iron_core.db"

def check():
    if not os.path.exists(DB_PATH):
        print(f"DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("--- Equity History (Last 5) ---")
    try:
        cursor.execute("SELECT * FROM equity_history ORDER BY id DESC LIMIT 5")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print(f"Error reading equity_history: {e}")

    print("\n--- Trades Today ---")
    try:
        cursor.execute("SELECT * FROM trades WHERE date(timestamp) = date('now')")
        rows = cursor.fetchall()
        print(f"Count: {len(rows)}")
        for row in rows[:5]:
            print(row)
    except Exception as e:
        print(f"Error reading trades: {e}")

    print("\n--- All Trades (Last 5) ---")
    try:
        cursor.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 5")
        for row in cursor.fetchall():
            print(row)
    except Exception as e:
        print(f"Error reading trades: {e}")

    conn.close()

if __name__ == "__main__":
    check()
