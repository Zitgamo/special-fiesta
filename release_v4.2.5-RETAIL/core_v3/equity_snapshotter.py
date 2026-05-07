import MetaTrader5 as mt5
import sqlite3
import json
import time
from datetime import datetime
from binance.client import Client

# Configuration
DB_PATH = "core_v3/iron_core.db"
SECRETS_PATH = "core_v3/secrets.json"

def get_binance_equity(api_key, api_secret):
    try:
        client = Client(api_key, api_secret)
        # Get Futures Balance
        info = client.futures_account()
        total_wallet_balance = float(info['totalWalletBalance'])
        total_unrealized_pnl = float(info['totalUnrealizedProfit'])
        total_margin_balance = float(info['totalMarginBalance'])
        return total_wallet_balance, total_margin_balance
    except Exception as e:
        print(f"Error fetching Binance equity: {e}")
        return 0.0, 0.0

def get_mt5_equity():
    try:
        if not mt5.initialize():
            print("MT5 Initialization Failed")
            return 0.0, 0.0
        
        account_info = mt5.account_info()
        if account_info is None:
            return 0.0, 0.0
            
        return account_info.balance, account_info.equity
    except Exception as e:
        print(f"Error fetching MT5 equity: {e}")
        return 0.0, 0.0
    finally:
        mt5.shutdown()

def log_equity():
    # Load Secrets
    with open(SECRETS_PATH, 'r') as f:
        secrets = json.load(f)
    
    # Get MT5 Data
    mt5_balance, mt5_equity = get_mt5_equity()
    
    # Get Binance Data
    binance_balance, binance_equity = get_binance_equity(
        secrets['binance_api_key'], 
        secrets['binance_api_secret']
    )
    
    total_balance = mt5_balance + binance_balance
    total_equity = mt5_equity + binance_equity
    
    if total_balance == 0:
        print("Total Balance is 0, skipping snapshot.")
        return

    drawdown = ((total_balance - total_equity) / total_balance) * 100 if total_balance > 0 else 0.0
    
    # Save to DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO equity_history (balance, equity, drawdown, timestamp)
        VALUES (?, ?, ?, ?)
    """, (total_balance, total_equity, drawdown, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    
    print(f"--- EQUITY SNAPSHOT TAKEN ---")
    print(f"Balance: ${total_balance:.2f} | Equity: ${total_equity:.2f} | DD: {drawdown:.2f}%")

if __name__ == "__main__":
    log_equity()
