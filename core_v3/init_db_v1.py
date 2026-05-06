import sqlite3
import os

DB_PATH = "core_v3/iron_core.db"

def init_safety_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create hq_config table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hq_config (
            key TEXT PRIMARY KEY,
            value TEXT,
            description TEXT,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Initialize GLOBAL_PAUSE if not exists
    cursor.execute("INSERT OR IGNORE INTO hq_config (key, value, description) VALUES ('GLOBAL_PAUSE', '0', 'Global emergency stop flag')")
    
    # Initialize CORE_MODE if not exists (0=Demo/Paper, 1=Real)
    cursor.execute("INSERT OR IGNORE INTO hq_config (key, value, description) VALUES ('CORE_MODE', '0', '0=Demo, 1=Real')")
    
    conn.commit()
    conn.close()
    print("[OK] hq_config table initialized and seeded.")

if __name__ == "__main__":
    init_safety_table()
