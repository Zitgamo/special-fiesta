import sqlite3
import os

db_path = 'core_v3/iron_core.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cursor.fetchall()]
    print(f"Tables found: {tables}")
    
    # Try common config table names
    target_table = None
    if 'config' in tables: target_table = 'config'
    elif 'hq_config' in tables: target_table = 'hq_config'
    
    if target_table:
        cursor.execute(f"INSERT OR REPLACE INTO {target_table} (key, value) VALUES ('DEPLOY_MODE', 'REAL')")
        conn.commit()
        print(f"SUCCESS: DEPLOY_MODE set to REAL in {target_table}")
    else:
        print("Error: No config table found.")
    conn.close()
else:
    print(f"Error: Database not found at {db_path}")
