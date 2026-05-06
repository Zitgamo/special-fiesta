import os
import sys
import time
from vnstock import Quote
import pandas as pd
import numpy as np
import talib
import logging
import json
from datetime import datetime, timedelta

# --- CONFIG ---
SYMBOL = "VN30F1M" # Automatic rolling handled by vnstock v4
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "03_DATA")
TRADES_CSV = os.path.join(DATA_DIR, "vn30_paper_trades.csv")
STATE_JSON = os.path.join(DATA_DIR, "vn30_active_pos.json")
LOG_FILE = "southern_bridge.log"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SOUTHERN_BRIDGE")

# --- DATA FETCH (STEALTH VCI) ---
def fetch_vn30_lightning():
    """
    Sovereign Stealth Fetch via vnstock v4 (VCI Source).
    Bypasses Entrade/DNSE auth walls entirely.
    """
    try:
        quote = Quote(symbol=SYMBOL, source='VCI')
        # Fetch last 200 bars to ensure technical indicators (EMA/ATR) are stable
        df = quote.history(length="200b", interval='1m')
        
        if df is not None and not df.empty:
            # We skip renaming here and let prepare_index_df handle it robustly
            return df
        else:
            logger.warning(f"Empty dataframe from vnstock VCI for {SYMBOL}")
    except Exception as e:
        logger.error(f"vnstock VCI Fetch Failed: {e}")
    return None

# --- DNA v7 LOGIC (Simplified for Index) ---
def prepare_index_df(df):
    """
    Robust column mapping and numeric conversion.
    Handles both legacy (open, high, low) and already-renamed (o, h, l) formats.
    """
    mapping = {
        'open': 'o', 'high': 'h', 'low': 'l', 'close': 'c', 'volume': 'v',
        'Open': 'o', 'High': 'h', 'Low': 'l', 'Close': 'c', 'Volume': 'v',
        'time': 'Datetime', 'Time': 'Datetime'
    }
    df = df.rename(columns=mapping)
    
    # Required columns for technical indicators
    required = ['o', 'h', 'l', 'c']
    for col in required:
        if col not in df.columns:
            logger.error(f"Missing required column: {col}. Available: {df.columns.tolist()}")
            return None
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    if 'v' in df.columns:
        df['v'] = pd.to_numeric(df['v'], errors='coerce')
        
    return df.dropna()

class SouthernPaperBridge:
    def __init__(self):
        self.logger = logger
        self.logger.info("Southern Front Bridge Initializing...")
        
        # Unit Configurations (Mapped to Sovereign DNA)
        self.units = {
            "SOUTH_ALPHA": {
                "name": "MOMENTUM_SCALPER",
                "ema_f": 20, "ema_s": 50, "atr_sl": 2.5, "atr_tp": 10.0,
                "pos": 0, "entry": 0, "entry_t": None, "sl": 0, "tp": 0
            },
            "SOUTH_OMEGA": {
                "name": "MEAN_REVERSION",
                "ema_f": 50, "ema_s": 100, "atr_sl": 1.5, "atr_tp": 5.0,
                "pos": 0, "entry": 0, "entry_t": None, "sl": 0, "tp": 0
            },
            "SOUTH_GAMMA": {
                "name": "TREND_FOLLOWER",
                "ema_f": 10, "ema_s": 30, "atr_sl": 1.5, "atr_tp": 6.0,
                "pos": 0, "entry": 0, "entry_t": None, "sl": 0, "tp": 0
            }
        }
        
        # --- PERSISTENT BALANCE ---
        self.current_balance_vnd = 100000000
        try:
            import sqlite3
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iron_core.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT equity FROM equity_history WHERE equity > 1000000 ORDER BY id DESC LIMIT 1")
            res = cursor.fetchone()
            if res: self.current_balance_vnd = res[0]
            conn.close()
            self.logger.info(f" >> [WALLET] Resumed Southern Balance: {self.current_balance_vnd:,.0f} VND")
        except: pass
        
        # Load existing state if available
        if os.path.exists(STATE_JSON):
            try:
                with open(STATE_JSON, "r") as f:
                    saved_units = json.load(f)
                    for uid, data in saved_units.items():
                        if uid in self.units:
                            self.units[uid].update(data)
                    self.logger.info(f" >> [RESTORE] Resumed Dragon Fleet from state file.")
            except: pass

        if not os.path.exists(TRADES_CSV):
            pd.DataFrame(columns=['unit_id', 'entry_t', 'exit_t', 'side', 'entry_p', 'exit_p', 'pnl_pts', 'reason']).to_csv(TRADES_CSV, index=False)

    def log_trade(self, unit_id, trade):
        # 1. Log to CSV (Local Backup)
        trade['unit_id'] = unit_id
        df = pd.DataFrame([trade])
        df.to_csv(TRADES_CSV, mode='a', header=False, index=False)
        
        # 2. Log to SQL
        try:
            import sqlite3
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iron_core.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO trades (unit_id, symbol, side, volume, price, sl, tp, sl_mult, tp_mult, er_at_entry, type, pnl, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', '+7 hours'))
            """, (
                unit_id, SYMBOL, trade['side'], 1.0, 
                trade['entry_p'], trade['sl'], trade['tp'], 
                trade.get('sl_mult'), trade.get('tp_mult'), trade.get('er_at_entry'),
                "PAPER", trade['pnl_pts']
            ))
            
            conn.commit()
            conn.close()
            
            # --- AUTO-LEARN ---
            from forensics import IronForensics
            f_sys = IronForensics()
            f_sys.record_learning(unit_id, SYMBOL, trade['side'], trade.get('sl_mult'), trade.get('tp_mult'), 
                                 trade.get('er_at_entry'), trade['pnl_pts'], 
                                 atr=trade.get('vol_atr', 0), spread=trade.get('spread_ratio', 0), 
                                 session=trade.get('session', 'ASIA'))
            
            self.logger.info(f" [SQL_SYNC] {unit_id} Strike recorded to iron_core.db")
            
            # --- COMPOUND EQUITY ---
            VND_PER_PT = 100000
            self.current_balance_vnd += (trade['pnl_pts'] * VND_PER_PT)
            self.logger.info(f" [WALLET_UPDATE] New Balance: {self.current_balance_vnd:,.0f} VND")
            
        except Exception as e:
            self.logger.error(f" !! [SQL_ERR] Could not sync paper trade: {e}")

        self.logger.info(f" [PAPER_STRIKE] {unit_id} {trade['side']} PnL: {trade['pnl_pts']:.2f} pts")

    def export_state(self, price):
        VND_PER_PT = 100000
        state = {}
        for uid, u in self.units.items():
            pnl_pts = round((price - u['entry']) * u['pos'], 2) if u['pos'] != 0 else 0
            state[uid] = {
                "pos": u['pos'],
                "entry": u['entry'],
                "sl": u['sl'],
                "tp": u['tp'],
                "entry_t": u['entry_t'],
                "pnl_pts": pnl_pts,
                "pnl_vnd": pnl_pts * VND_PER_PT,
                "equity_vnd": self.current_balance_vnd + (pnl_pts * VND_PER_PT),
                "active": u['pos'] != 0
            }
        with open(STATE_JSON, "w") as f:
            json.dump(state, f, indent=4)
        
        self.record_equity_snapshot(price)

    def record_equity_snapshot(self, price):
        """Records a point in the equity history for the Southern Front."""
        try:
            VND_PER_PT = 100000
            current_float_pts = sum((price - u['entry']) * u['pos'] for u in self.units.values() if u['pos'] != 0)
            current_equity = self.current_balance_vnd + (current_float_pts * VND_PER_PT)
            
            import sqlite3
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iron_core.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            drawdown = (current_float_pts * VND_PER_PT / self.current_balance_vnd) * 100 if self.current_balance_vnd != 0 else 0
            
            cursor.execute("""
                INSERT INTO equity_history (balance, equity, drawdown, timestamp)
                VALUES (?, ?, ?, datetime('now', '+7 hours'))
            """, (self.current_balance_vnd, current_equity, drawdown))
            conn.commit()
            conn.close()
        except: pass

    def run_cycle(self):
        df_raw = fetch_vn30_lightning()
        if df_raw is None or len(df_raw) < 60: return
        
        df_raw = prepare_index_df(df_raw)
        if df_raw is None or df_raw.empty: return
        
        price = df_raw['c'].iloc[-1]
        now_t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for uid, u in self.units.items():
            df = df_raw.copy()
            df['ema_f'] = talib.EMA(df['c'].values, u['ema_f'])
            df['ema_s'] = talib.EMA(df['c'].values, u['ema_s'])
            df['atr'] = talib.ATR(df['h'].values, df['l'].values, df['c'].values, 14)
            
            last = df.iloc[-1]
            atr = last['atr']
            ema_f = last['ema_f']
            ema_s = last['ema_s']
            
            # --- MONITOR ---
            if u['pos'] != 0:
                pnl = (price - u['entry']) * u['pos']
                hit = False
                reason = ""
                
                if u['pos'] == 1:
                    if price <= u['sl']: hit = True; reason = "SL"
                    elif price >= u['tp']: hit = True; reason = "TP"
                else:
                    if price >= u['sl']: hit = True; reason = "SL"
                    elif price <= u['tp']: hit = True; reason = "TP"
                
                if (u['pos'] == 1 and price < ema_s) or (u['pos'] == -1 and price > ema_s):
                    hit = True; reason = "TREND_FLIP"

                if hit:
                    self.log_trade(uid, {
                        'entry_t': u['entry_t'], 'exit_t': now_t,
                        'symbol': SYMBOL,
                        'side': 'LONG' if u['pos'] == 1 else 'SHORT',
                        'entry_p': u['entry'], 'exit_p': price,
                        'pnl_pts': round(pnl, 2), 'reason': reason,
                        'sl': u['sl'], 'tp': u['tp'],
                        'sl_mult': u.get('sl_mult'), 'tp_mult': u.get('tp_mult'),
                        'er_at_entry': u.get('er_at_entry')
                    })
                    u['pos'] = 0

            # --- ENTRY ---
            if u['pos'] == 0:
                side = 0
                if price > ema_f > ema_s: side = 1
                elif price < ema_f < ema_s: side = -1
                
                if side != 0:
                    # --- ADAPTIVE TARGETS ---
                    from optimizer import SovereignOptimizer
                    from analytics import IronAnalytics
                    
                    er = IronAnalytics.get_efficiency_ratio(SYMBOL)
                    optimizer = SovereignOptimizer()
                    
                    # Mutate targets based on market condition
                    s_id = "BUY" if side == 1 else "SELL"
                    sl_mult, tp_mult = optimizer.optimize_targets(SYMBOL, price, atr, s_id, er=er)
                    
                    # Capture Context (F1M is always ASIA)
                    utc_hour = datetime.utcnow().hour
                    session = "ASIA" # F1M is localized
                    spread_ratio = 0.05 # Conservative estimate for F1M
                    
                    u['pos'] = side
                    u['entry'] = price
                    u['entry_t'] = now_t
                    u['sl'] = price - (atr * sl_mult * side)
                    u['tp'] = price + (atr * tp_mult * side)
                    
                    # Store multipliers for learning
                    u['sl_mult'] = sl_mult
                    u['tp_mult'] = tp_mult
                    u['er_at_entry'] = er
                    u['vol_atr'] = atr
                    u['session'] = session
                    u['spread_ratio'] = spread_ratio
                    
                    self.logger.info(f" [{uid}] ENTRY {'LONG' if side==1 else 'SHORT'} @ {price} | SL: {u['sl']:.1f} ({sl_mult}x) TP: {u['tp']:.1f} ({tp_mult}x) | ER: {er}")

        self.export_state(price)


    def start(self):
        self.logger.info("Southern Front Expansion: Online.")
        while True:
            try:
                # Check Market Hours (Vietnam: 08:45 - 11:30, 13:00 - 15:00)
                now = datetime.now()
                # Simplified check for testing
                self.run_cycle()
            except Exception as e:
                self.logger.error(f"Bridge Cycle Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    bridge = SouthernPaperBridge()
    bridge.start()
