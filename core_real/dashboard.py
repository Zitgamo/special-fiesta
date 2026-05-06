import sqlite3
import time
import os
import json

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_status():
    try:
        conn = sqlite3.connect("iron_core.db")
        cursor = conn.cursor()
        
        # 1. Account Health
        cursor.execute("SELECT balance, equity, drawdown, timestamp FROM equity_history ORDER BY id DESC LIMIT 1")
        health = cursor.fetchone()
        
        # 2. Recent Trades
        cursor.execute("SELECT unit_id, symbol, side, price, timestamp FROM trades ORDER BY id DESC LIMIT 5")
        trades = cursor.fetchall()
        
        # 3. DNA Status
        with open("core_v3/dna.json", "r") as f:
            dna = json.load(f)
            
        conn.close()
        return health, trades, dna
    except:
        return None, [], {}

def render_hud():
    while True:
        health, trades, dna = get_status()
        clear_console()
        
        print("================================================================")
        print("          IRON COMMANDER // FORENSIC HUD v3.0                  ")
        print("================================================================")
        
        if health:
            bal, eq, dd, ts = health
            print(f" [ACCOUNT] BALANCE: ${bal:,.2f} | EQUITY: ${eq:,.2f} | DD: {dd*100:.2f}%")
            print(f" [LAST_UPD]: {ts}")
        
        print("\n [UNIT_DNA_BLUEPRINTS]")
        for unit, params in dna.items():
            print(f"  >> {unit:6} | SL: {params['SL']:.2f} | TP: {params['TP']:.2f} | LOT: {params['LOT_SIZE']:.3f}")
            
        print("\n [RECENT_STRIKES]")
        if not trades:
            print("  >> NO STRIKES RECORDED.")
        for t in trades:
            print(f"  >> {t[4][11:19]} | {t[0]:6} | {t[2]:4} {t[1]:8} @ {t[3]:,.2f}")
            
        print("\n================================================================")
        print(" [SYSTEM]: DUAL-CORE ACTIVE | REGIME: DYNAMIC | SHIELD: ON")
        print("================================================================")
        
        time.sleep(15)

if __name__ == "__main__":
    render_hud()
