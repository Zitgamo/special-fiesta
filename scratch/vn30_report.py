import pandas as pd
import os
from datetime import datetime

csv_path = "03_DATA/vn30_paper_trades.csv"
if not os.path.exists(csv_path):
    print("CSV NOT FOUND")
    exit()

# Load CSV without header as per the snapshot
try:
    df = pd.read_csv(csv_path, header=None, names=[
        "entry_time", "exit_time", "symbol", "side", "entry", "exit", "pnl", "reason", "sl", "tp", "sl_mult", "tp_mult", "er", "unit"
    ])
    
    # Ensure pnl is numeric
    df['pnl'] = pd.to_numeric(df['pnl'], errors='coerce')
    
    # Filter for today (2026-05-06)
    today = "2026-05-06"
    df_today = df[df['entry_time'].astype(str).str.contains(today)]
    
    total_pnl = df_today['pnl'].sum()
    total_trades = len(df_today)
    wins = len(df_today[df_today['pnl'] > 0])
    losses = len(df_today[df_today['pnl'] < 0])
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    total_vnd = total_pnl * 100000
    
    print(f"--- VN30F1M PERFORMANCE REPORT ({today}) ---")
    print(f"Total Trades: {total_trades}")
    print(f"Wins: {wins} | Losses: {losses}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Total PnL (Points): {total_pnl:.2f}")
    print(f"Total PnL (VND): {total_vnd:,.0f} VND")
    
    print("\n--- UNIT BREAKDOWN ---")
    units = df_today['unit'].unique()
    for unit in units:
        unit_df = df_today[df_today['unit'] == unit]
        u_pnl = unit_df['pnl'].sum()
        u_trades = len(unit_df)
        u_wins = len(unit_df[unit_df['pnl'] > 0])
        u_wr = (u_wins / u_trades * 100) if u_trades > 0 else 0
        print(f"[{unit}] Trades: {u_trades} | WinRate: {u_wr:.2f}% | PnL: {u_pnl:.2f} pts")
    
    print("\n--- RECENT TRADES ---")
    print(df_today.tail(10)[['side', 'entry', 'exit', 'pnl', 'reason', 'unit']])

except Exception as e:
    print(f"Error: {e}")
