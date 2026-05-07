import sqlite3
import pandas as pd
import os
import sys
from datetime import datetime

def export_unit_data(unit_id, db_path="core_v3/iron_core.db", export_dir="03_DATA/R&D"):
    """
    Extracts all trade data for a specific unit for Data Science analysis.
    """
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{unit_id}_{timestamp}.csv"
    filepath = os.path.join(export_dir, filename)
    
    print(f" >> [RESEARCH] Initiating Data Extraction for Unit: {unit_id}...")
    
    try:
        conn = sqlite3.connect(db_path)
        # Select all relevant columns for R&D
        query = f"""
            SELECT * FROM trades 
            WHERE unit_id = '{unit_id}'
            ORDER BY timestamp ASC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if df.empty:
            print(f" !! [EMPTY] No trade records found for unit {unit_id}.")
            return None
        
        df.to_csv(filepath, index=False)
        print(f" >> [SUCCESS] Exported {len(df)} records to {filepath}")
        return filepath
        
    except Exception as e:
        print(f" !! [ERROR] Extraction failed: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python research_export.py [UNIT_ID]")
    else:
        target_unit = sys.argv[1]
        export_unit_data(target_unit)
