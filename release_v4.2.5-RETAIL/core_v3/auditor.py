import sqlite3
import pandas as pd

def generate_audit_report():
    print("--- SOVEREIGN AUDITOR: COMMENCING FORENSIC ANALYSIS ---")
    try:
        conn = sqlite3.connect("iron_core.db")
        
        # 1. Unit Performance Audit
        df_trades = pd.read_sql_query("SELECT * FROM trades", conn)
        if df_trades.empty:
            print(" >> [AUDIT] No trade history found. Insufficient data for veterancy.")
            return

        print("\n [UNIT_VETERANCY_REPORT]")
        perf = df_trades.groupby('unit_id').size().reset_index(name='total_strikes')
        print(perf.to_string(index=False))
        
        # 2. Equity Growth Audit
        df_equity = pd.read_sql_query("SELECT * FROM equity_history", conn)
        if not df_equity.empty:
            start_bal = df_equity['balance'].iloc[0]
            end_bal = df_equity['balance'].iloc[-1]
            growth = ((end_bal - start_bal) / start_bal) * 100
            print(f"\n [EQUITY_SUMMARY]")
            print(f"  >> INITIAL BALANCE: ${start_bal:,.2f}")
            print(f"  >> CURRENT BALANCE: ${end_bal:,.2f}")
            print(f"  >> GROWTH: {growth:+.2f}%")
            
        conn.close()
    except Exception as e:
        print(f" !! [AUDIT_ERR] {e}")

if __name__ == "__main__":
    generate_audit_report()
