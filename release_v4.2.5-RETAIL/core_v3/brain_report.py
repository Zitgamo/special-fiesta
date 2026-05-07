import sqlite3
import pandas as pd
import os

DB_PATH = r"c:\Users\ADMIN\Desktop\IRON_COMMANDER_ELITE\core_v3\iron_core.db"

def generate_report():
    print("="*60)
    print("SOVEREIGN BRAIN REPORT - Empirical Wisdom Summary")
    print("="*60)
    
    if not os.path.exists(DB_PATH):
        print("DB not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    
    # 1. Overall Statistics
    query_total = "SELECT COUNT(*) FROM empirical_learning"
    total_samples = conn.execute(query_total).fetchone()[0]
    
    print(f" TOTAL EXPERIENCE SAMPLES: {total_samples}")
    print("-" * 60)
    
    if total_samples == 0:
        print(" [INFO] Brain is still in 'Infancy'. No trades recorded yet.")
        print(" Once trades close, this report will show the best SL/TP clusters.")
        conn.close()
        return

    # 2. Best SL/TP Clusters by Symbol
    query_best = """
        SELECT symbol, sl_mult, tp_mult, COUNT(*) as trades, AVG(outcome_pnl) as avg_pnl
        FROM empirical_learning
        GROUP BY symbol, sl_mult, tp_mult
        HAVING trades >= 1
        ORDER BY avg_pnl DESC
        LIMIT 10
    """
    df_best = pd.read_sql_query(query_best, conn)
    
    print(" TOP PERFORMING TARGET CONFIGS:")
    print(df_best.to_string(index=False))
    print("-" * 60)

    # 3. Efficiency Ratio Correlation
    query_er = """
        SELECT 
            CASE 
                WHEN er_at_entry < 0.3 THEN 'LOW (Ranging)'
                WHEN er_at_entry BETWEEN 0.3 AND 0.6 THEN 'MED (Transition)'
                ELSE 'HIGH (Trending)'
            END as regime,
            AVG(outcome_pnl) as avg_pnl,
            COUNT(*) as trades
        FROM empirical_learning
        GROUP BY regime
    """
    df_er = pd.read_sql_query(query_er, conn)
    print(" PERFORMANCE BY MARKET REGIME (ER):")
    print(df_er.to_string(index=False))
    
    conn.close()
    print("="*60)

if __name__ == "__main__":
    generate_report()
