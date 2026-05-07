import sqlite3
import pandas as pd
import numpy as np

def run_audit():
    conn = sqlite3.connect('core_v3/iron_core.db')
    df = pd.read_sql_query('SELECT unit_id, symbol, pnl, er_at_entry, type FROM trades WHERE pnl IS NOT NULL', conn)
    conn.close()

    if df.empty:
        print(" !! [AUDIT_ERR] No trade data found.")
        return

    df['is_win'] = df['pnl'] > 0
    
    # 1. SEGMENT BY EFFICIENCY (ER)
    high_er = df[df['er_at_entry'] > 0.6].copy()
    mid_er = df[(df['er_at_entry'] >= 0.4) & (df['er_at_entry'] <= 0.6)].copy()
    low_er = df[df['er_at_entry'] < 0.4].copy()

    print("="*50)
    print("SOVEREIGN FORENSIC PERFORMANCE AUDIT")
    print("="*50)
    print(f"Total Strikes Analyzed: {len(df)}")
    
    # 2. ANALYSIS TABLE
    def print_stats(label, sub_df):
        if sub_df.empty:
            print(f"\n[{label}] No data available.")
            return
        wr = sub_df['is_win'].mean() * 100
        total_pnl = sub_df['pnl'].sum()
        avg_er = sub_df['er_at_entry'].mean()
        print(f"\n[{label}]")
        print(f" - Count:      {len(sub_df)}")
        print(f" - Avg ER:     {avg_er:.2f}")
        print(f" - Win Rate:   {wr:.1f}%")
        print(f" - Net PnL:    ${total_pnl:,.2f}")

    print_stats("GOOD: HIGH-EFFICIENCY (TREND)", high_er)
    print_stats("NEUTRAL: MID-RANGE (TRANSITION)", mid_er)
    print_stats("BAD: LOW-EFFICIENCY (CHOP)", low_er)

    print("\n" + "="*50)
    print("TACTICAL CONCLUSION")
    print("="*50)
    if not high_er.empty and not low_er.empty:
        if high_er['is_win'].mean() > low_er['is_win'].mean():
            print("HYPOTHESIS CONFIRMED: High-ER strikes are the primary Alpha driver.")
            print("SDS v2.0 MANDATE: Correct. Focus all capital on >0.6 ER regimes.")
        else:
            print("HYPOTHESIS FRACTURED: Market characteristics have shifted.")
    print("="*50)

if __name__ == "__main__":
    run_audit()
