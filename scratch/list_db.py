import sqlite3
import os

DB_PATH = r"c:\Users\ADMIN\Desktop\IRON_COMMANDER_ELITE\core_v3\iron_core.db"

def list_tables():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table in tables:
        t_name = table[0]
        print(f"\n--- TABLE: {t_name} ---")
        cursor.execute(f"PRAGMA table_info({t_name})")
        for col in cursor.fetchall():
            print(f"  {col[1]} ({col[2]})")
            
    conn.close()

if __name__ == "__main__":
    list_tables()
