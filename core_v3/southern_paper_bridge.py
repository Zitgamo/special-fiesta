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
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analytics import IronAnalytics

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
logger = logging.getLogger("DRAGON_BRIDGE")

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
        self.logger.info("Vietnam Hàng Da Front Bridge Initializing...")
        
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
        
        # DNA Handshake
        try:
            with open("core_v3/dna.json", "r") as f:
                self.dna = json.load(f)
        except:
            self.dna = {}

        # --- HIGH COUNCIL HANDSHAKE (v9.0) ---
        self.verdict_file = os.path.join(DATA_DIR, "council_verdict.json")
        self.council_overrides = {}
        self.load_council_advice()

        # --- UPTIME SENTINEL (v10.1) ---
        self.start_time = datetime.now()
        
        if not os.path.exists(TRADES_CSV):
            pd.DataFrame(columns=['unit_id', 'entry_t', 'exit_t', 'side', 'entry_p', 'exit_p', 'pnl_pts', 'reason']).to_csv(TRADES_CSV, index=False)
        
        # --- SOVEREIGN VICTORY METRICS (v11.0) ---
        self.peak_equity = self.current_balance_vnd
        self.max_drawdown_vnd = 0
        self.trade_stats = {"total": 0, "wins": 0, "losses": 0, "last_t": None}
        self.prophecy_breach_active = False
        
        # --- INITIAL PULSE ---
        self.export_state(0)

        # --- CIRCUIT BREAKER STATE (v9.6) ---
        self.daily_pnl = 0
        self.last_pnl_reset = datetime.now().date()
        self.is_dormant = False

    def load_council_advice(self):
        """Loads the tactical overrides from the High Council LLM."""
        if os.path.exists(self.verdict_file):
            try:
                with open(self.verdict_file, "r") as f:
                    verdict = json.load(f)
                    self.council_overrides = verdict.get("overrides", {})
                    self.logger.info(f" >> [COUNCIL] Applied Tactical Advice: {verdict.get('council_advice')}")
            except Exception as e:
                self.logger.error(f" !! [COUNCIL_ERR] Failed to load verdict: {e}")

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
            
            # --- VICTORY TRADE STATS (v11.0) ---
            self.trade_stats['total'] += 1
            if trade['pnl_pts'] > 0: self.trade_stats['wins'] += 1
            else: self.trade_stats['losses'] += 1
            self.trade_stats['last_t'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # --- COMPOUND EQUITY ---
            VND_PER_PT = 100000
            self.current_balance_vnd += (trade['pnl_pts'] * VND_PER_PT)
            self.logger.info(f" [WALLET_UPDATE] New Balance: {self.current_balance_vnd:,.0f} VND")
            
        except Exception as e:
            self.logger.error(f" !! [SQL_ERR] Could not sync paper trade: {e}")

        self.logger.info(f" [PAPER_STRIKE] {unit_id} {trade['side']} PnL: {trade['pnl_pts']:.2f} pts")

    def trigger_immediate_breach_alert(self, price, min_b, max_b):
        """Immediately bypasses the 'x2' interval to alert the Commander of a Prophecy Breach."""
        self.logger.warning(f" !! [PROPHECY_BREACH] Price {price} broke boundaries [{min_b}-{max_b}]!")
        try:
            from fleet_report import FleetReporter
            reporter = FleetReporter()
            # Send the dedicated Council Breach Card (v12.0)
            reporter.send_council_report(is_breach=True)
        except Exception as e:
            self.logger.error(f" !! [ALERT_FAIL] Could not send breach alert: {e}")

    def export_state(self, price):
        VND_PER_PT = 100000
        now_t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Uptime Calculation
        uptime = datetime.now() - self.start_time
        uptime_str = str(uptime).split('.')[0] # HH:MM:SS
        
        # --- VICTORY METRICS CALCULATION (v11.0) ---
        total_pnl_pts = 0
        for uid, u in self.units.items():
            if u['pos'] != 0:
                total_pnl_pts += (price - u['entry']) * u['pos']
        
        current_equity_vnd = self.current_balance_vnd + (total_pnl_pts * VND_PER_PT)
        
        # Track Peak & DD
        if current_equity_vnd > self.peak_equity:
            self.peak_equity = current_equity_vnd
        
        drawdown_vnd = self.peak_equity - current_equity_vnd
        if drawdown_vnd > self.max_drawdown_vnd:
            self.max_drawdown_vnd = drawdown_vnd
            
        # Check Prophecy Breach
        breach_msg = "SAFE ✅"
        try:
            with open(os.path.join(DATA_DIR, "council_verdict.json"), "r") as f:
                v = json.load(f)
                min_b = v.get('min_boundary', 0)
                max_b = v.get('max_boundary', 0)
                if min_b > 0 and (price < min_b or price > max_b) and price > 0:
                    breach_msg = f"⚠️ BREACH: {price:.1f} is outside [{min_b}-{max_b}]"
                    if not self.prophecy_breach_active:
                        self.prophecy_breach_active = True
                        self.trigger_immediate_breach_alert(price, min_b, max_b)
                elif min_b > 0 and price >= min_b and price <= max_b:
                    self.prophecy_breach_active = False
        except: pass

        state = {
            "meta": {
                "uptime": uptime_str, 
                "last_update": now_t,
                "peak_equity": self.peak_equity,
                "max_dd_vnd": self.max_drawdown_vnd,
                "current_dd_vnd": drawdown_vnd,
                "trade_stats": self.trade_stats,
                "breach_status": breach_msg
            }
        }
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
                "active": u['pos'] != 0,
                # --- CONTEXT PERSISTENCE ---
                "sl_mult": u.get('sl_mult'),
                "tp_mult": u.get('tp_mult'),
                "er_at_entry": u.get('er_at_entry'),
                "vol_atr": u.get('vol_atr'),
                "session": u.get('session'),
                "spread_ratio": u.get('spread_ratio')
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

    def check_circuit_breaker(self):
        """Ensures the bot stays silent if the daily loss limit is hit."""
        today = datetime.now().date()
        if today > self.last_pnl_reset:
            self.daily_pnl = 0
            self.last_pnl_reset = today
            self.is_dormant = False
            self.logger.info(" >> [RESET] New Day. Circuit Breaker Reset.")

        if self.daily_pnl <= -15.0:
            if not self.is_dormant:
                self.logger.error(" !! [CIRCUIT_BREAKER] Daily Loss Limit Reached (-15.0 pts). Entering Dormancy.")
                self.is_dormant = True
                # Flatten all units
                for uid, u in self.units.items():
                    if u['pos'] != 0: u['pos'] = 0 # Emergency Flat
            return True
        return False

    def run_cycle(self):
        if self.check_circuit_breaker(): return
        df_raw = fetch_vn30_lightning()
        if df_raw is None or len(df_raw) < 60: return
        
        df_raw = prepare_index_df(df_raw)
        if df_raw is None or df_raw.empty: return
        
        price = df_raw['c'].iloc[-1]
        
        # --- PROPHETIC WATCHDOG (v9.1) ---
        min_b = self.council_overrides.get("min_boundary", 0)
        max_b = self.council_overrides.get("max_boundary", 99999)
        
        if price < min_b or price > max_b:
            self.logger.warning(f" !! [BREAKOUT] Price {price} breached prophecy [{min_b}, {max_b}]. Consulting Council...")
            # Event-Driven Trigger: Run the Auditor/Counselor
            os.system("python core_v3/high_council.py")
            self.load_council_advice()
            # Update boundaries immediately to prevent infinite loop
            min_b = self.council_overrides.get("min_boundary", 0)
            max_b = self.council_overrides.get("max_boundary", 99999)

        now_t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Council Sensitivity Overrides
        gov_sens = self.council_overrides.get("governor_sensitivity", 1.0)
        
        for uid, u in self.units.items():
            df = df_raw.copy()
            # --- ORACLE BRAIN SCAN (SI v5.0) ---
            bias, er, vel = IronAnalytics.get_bias(df)
            
            # Apply Governor Sensitivity (Veto Logic)
            if gov_sens > 1.0 and er < (0.15 * gov_sens):
                bias = "NEUTRAL" # Council Veto due to low efficiency
            
            atr = talib.ATR(df['h'].values, df['l'].values, df['c'].values, 14).iloc[-1]
            
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
                
                if (u['pos'] == 1 and bias == "BEARISH") or (u['pos'] == -1 and bias == "BULLISH"):
                    hit = True; reason = "BIAS_FLIP"

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
                if bias == "BULLISH" and er > 0.3: side = 1
                elif bias == "BEARISH" and er > 0.3: side = -1
                
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
                    u['sl'] = round(price - (atr * sl_mult * side), 1)
                    u['tp'] = round(price + (atr * tp_mult * side), 1)
                    
                    # Store multipliers for learning
                    u['sl_mult'] = sl_mult
                    u['tp_mult'] = tp_mult
                    u['er_at_entry'] = er
                    u['vol_atr'] = atr
                    u['session'] = session
                    u['spread_ratio'] = spread_ratio
                    
                    self.logger.info(f" [{uid}] ENTRY {'LONG' if side==1 else 'SHORT'} @ {price} | SL: {u['sl']:.1f} ({sl_mult}x) TP: {u['tp']:.1f} ({tp_mult}x) | ER: {er}")
                    
                    # --- SIGNAL RELAY (ALPHA ONLY as per User Request) ---
                    if uid == "SOUTH_ALPHA":
                        # Quarantine Check: Do not spam Tele if not good enough
                        if self.dna.get("SOUTH_ALPHA", {}).get("QUARANTINE"):
                            self.logger.info(f" >> [QUARANTINE_SUPPRESS] Skipping Telegram signal for {SYMBOL} (Unit in Re-R&D).")
                        else:
                            try:
                                from signal_commander import SignalCommander
                                sc = SignalCommander()
                                sc.send_signal(SYMBOL, s_id, price, u['sl'], u['tp'], er, lot=1.0, reason="South Alpha (Index Strike)")
                            except Exception as sig_err:
                                self.logger.error(f" !! [SIGNAL_ERR] Failed to relay South Alpha strike: {sig_err}")

        self.export_state(price)


    def start(self):
        self.logger.info("Southern Front Expansion: Online.")
        loop_count = 0
        while True:
            try:
                # ... existing logic ...
                now = datetime.now()
                h, m = now.hour, now.minute
                
                is_open = False
                if (h == 8 and m >= 45) or (9 <= h < 11) or (h == 11 and m <= 30):
                    is_open = True
                elif (13 <= h < 14) or (h == 14 and m <= 45):
                    is_open = True
                
                if is_open:
                    self.run_cycle()
                else:
                    # Market Closed: Clear all paper positions for the day
                    has_pos = any(u['pos'] != 0 for u in self.units.values())
                    if has_pos:
                        self.logger.info(" !! [MARKET_END] VN30 Session Ended. Liquating all active paper positions.")
                        for uid, u in self.units.items():
                            if u['pos'] != 0:
                                u['pos'] = 0
                        self.export_state(0) # Final state save
                    
                    # Hibernate to save CPU
                    if loop_count % 60 == 0: # Log every hour during hibernation
                        self.logger.info(" >> [HIBERNATION] VN30 Market Closed. Waiting for next session (08:45 ICT).")
                
                loop_count += 1
            except Exception as e:
                self.logger.error(f"Bridge Cycle Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    bridge = SouthernPaperBridge()
    bridge.start()
