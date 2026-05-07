import time
import logging
import os
import json
from vault_v2 import IronVault
from bridges import IronBridges
from analytics import IronAnalytics
from forensics import IronForensics

class IronEngine:
    def __init__(self, secrets_path, unit_id='ALPHA'):
        self.unit_id = unit_id
        self.logger = self._setup_logging()
        self.bridges = IronBridges(secrets_path)
        self.forensics = IronForensics()
        from safety import IronSafety
        self.safety = IronSafety()
        self.is_running = True
        from paths import DNA_PATH
        self.dna_path = DNA_PATH
        self.dna = self._load_dna()
        self.tracker_path = f"core_v3/signal_tracker_{self.unit_id.lower()}.json"
        self.signal_tracker = self._load_tracker()
        
    def _load_dna(self):
        if os.path.exists(self.dna_path):
            try:
                with open(self.dna_path, 'r') as f:
                    return json.load(f)
            except: pass
        return {}
        
    def _load_tracker(self):
        if os.path.exists(self.tracker_path):
            try:
                with open(self.tracker_path, 'r') as f:
                    return json.load(f)
            except: pass
        return {}

    def _save_tracker(self):
        try:
            with open(self.tracker_path, 'w') as f:
                json.dump(self.signal_tracker, f)
        except: pass
    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler(f"{self.unit_id.lower()}_engine.log"),
                logging.StreamHandler()
            ]
        )
        # Pipe Bridge logs into Engine log
        bridge_logger = logging.getLogger("IronBridges")
        bridge_logger.addHandler(logging.FileHandler(f"{self.unit_id.lower()}_engine.log"))
        bridge_logger.setLevel(logging.INFO)
        
        return logging.getLogger("IRON_ENGINE")

    def run(self):
        self.logger.info("--- IRON CORE ENGINE v3.0 ACTIVE ---")
        
        while self.is_running:
            try:
                # 1. LIVE MT5 HANDSHAKE
                import MetaTrader5 as mt5
                
                # Silent Check: If already linked, don't disturb the terminal
                if not mt5.terminal_info():
                    self.logger.info(" >> [HANDSHAKE] Linking to active terminal...")
                    if not mt5.initialize():
                        # Only use path if silent init fails (Terminal likely closed)
                        path = r"C:\Program Files\MetaTrader 5 EXNESS\terminal64.exe"
                        if not mt5.initialize(path=path):
                            self.logger.warning(" !! [HANDSHAKE] Neural Link Fracture. Retrying...")
                            time.sleep(10)
                            continue

                # Account Audit
                account = mt5.account_info()
                if not account:
                    # Try a silent re-init in case of timeout
                    mt5.initialize()
                    account = mt5.account_info()
                    if not account:
                        self.logger.warning(" !! [ACCOUNT] No active account session found. Please login to MT5.")
                        time.sleep(10)
                        continue

                balance = account.balance
                equity = account.equity
                drawdown = (balance - equity) / balance if balance > 0 else 0
                
                print(f"\n[HEARTBEAT] {time.strftime('%H:%M:%S')}", flush=True)
                print(f" >> BALANCE: ${balance:,.2f} | EQUITY: ${equity:,.2f} | DD: {drawdown*100:.2f}%", flush=True)
                
                # 2. LOG SNAPSHOT
                self.forensics.log_snapshot(balance, equity, drawdown)

                # --- AUTO-JANITOR: Tactical maintenance if logs are "dirty" (> 5MB) ---
                log_file = f"{self.unit_id.lower()}_engine.log"
                if os.path.exists(log_file) and os.path.getsize(log_file) > 5 * 1024 * 1024:
                    self.logger.info(f" >> [MAINTENANCE] Log size exceeded 5MB. Triggering Auto-Janitor...")
                    try:
                        import sys
                        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                        from janitor import SovereignJanitor
                        janitor = SovereignJanitor()
                        janitor.cleanup_temp_files()
                        janitor.cleanup_old_logs(days=1)
                    except Exception as e:
                        self.logger.warning(f" !! [MAINTENANCE] Janitor failed: {e}")

                # 3. INITIALIZE VAULT (Dual-Front Aware)
                vault = IronVault(self.bridges)
                
                # 4. ACTIVE RISK GOVERNOR (Shaving & Stacking)
                vault.active_risk_governor(self.bridges, self)

                # 5. TACTICAL SCAN (Dynamic Squadron)
                try:
                    with open("core_v3/squadron.json", "r") as f:
                        squad = json.load(f)
                        symbols = squad.get(self.unit_id, ["XAUUSD", "BTCUSDT"])
                except:
                    symbols = ["XAUUSD", "BTCUSDT"]

                # --- DEMO BLACKLIST: skip trading restricted tickers on demo accounts ---
                blacklist = []
                try:
                    with open("core_v3/blacklist.json", "r") as bf:
                        blacklist = json.load(bf)
                except Exception:
                    blacklist = []
                    
                for symbol in symbols:
                    # --- DEMO BLACKLIST: skip trading restricted tickers on demo accounts ---
                    if symbol.upper() in [s.upper() for s in blacklist]:
                        self.logger.info(f" >> [BLACKLIST] Skipping restricted ticker: {symbol}")
                        continue

                    price = self.bridges.get_price(symbol)
                    if not price: continue

                    # --- MARKET HOURS FILTER (VN30F1M) ---
                    if "VN30" in symbol:
                        from datetime import datetime
                        import pytz
                        import time as pytime
                        from datetime import time as dt_time
                        vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                        vn_now = datetime.now(vn_tz).time()
                        is_open = (vn_now >= dt_time(8, 45) and vn_now <= dt_time(14, 45))
                        if not is_open:
                            self.logger.info(f" >> [HIBERNATION] VN Market Closed ({vn_now}). Skipping {symbol}...")
                            continue
                    
                    # 4. ANALYTICS (Session Bias + Volatility + Regime)
                    bias, dist = IronAnalytics.get_session_bias(symbol, bridges=self.bridges)
                    atr = IronAnalytics.get_atr(symbol, self.bridges)
                    er = IronAnalytics.get_efficiency_ratio(symbol, bridges=self.bridges)
                    
                    if not atr:
                        self.logger.warning(f" !! [DATA] ATR calculation failed for {symbol}. Skipping.")
                        continue

                    velocity = IronAnalytics.get_velocity(symbol, bridges=self.bridges)
                    self.logger.info(f"SCANNING: {symbol} | PRICE: {price:.2f} | BIAS: {bias} | ER: {er} | VEL: {velocity}")
                    
                    # 5. POSITION GUARD (Suffix-Aware)
                    all_pos = self.bridges.get_active_positions()
                    active_symbol_pos = [p for p in all_pos if symbol.upper() in p['symbol'].upper()]
                    has_pos = len(active_symbol_pos) > 0
                    
                    if has_pos:
                        self.logger.info(f" >> [GUARD] {symbol} position already active.")
                        
                        # --- ELITE HARVESTER v5.0 (Expectancy-Driven) ---
                        symbol_pnl = sum(p['pnl'] for p in active_symbol_pos)
                        max_layers = self.dna.get(self.unit_id, {}).get("ACTIVE_RISK", {}).get("MAX_LAYERS", 1)
                        
                        # Calculate Unit Expectancy
                        stats = {} # Default
                        wr_str = stats.get("win_rate", "50%").replace('%','')
                        wr = float(wr_str) / 100
                        expectancy = (wr * 2.0) - ((1-wr) * 1.0) # Simplified R:R proxy
                        
                        # Scaling is allowed if:
                        # 1. Expectancy is positive (> 0.2) OR it's OMEGA (aggressive)
                        # 2. We haven't reached MAX_LAYERS
                        # 3. We are NOT in the Milking zone (PnL < 3.0 ATR)
                        is_high_odds = expectancy > 0.2 or self.unit_id == "OMEGA"
                        in_milking_zone = symbol_pnl > (atr * 3.0) 
                        
                        if is_high_odds and not in_milking_zone and len(active_symbol_pos) < max_layers:
                            try:
                                target_pos = active_symbol_pos[0]
                                current_symbol = target_pos['symbol']
                                
                                # Cooldown Guard (15 minutes for high-odds)
                                last_scale = self.dna.get(self.unit_id, {}).get("LAST_SCALE", 0)
                                if time.time() - last_scale < 900:
                                    continue

                                self.logger.info(f" >> [HARVESTER] High Expectancy ({expectancy:.2f}). Scaling in Layer {len(active_symbol_pos)+1} on {current_symbol}...")
                                
                                info = mt5.symbol_info(current_symbol)
                                if info:
                                    min_lot = info.volume_min
                                    v_step = info.volume_step
                                    base_lot = target_pos['volume']
                                    
                                    # Dynamic Scale Lot based on confidence
                                    scale_ratio = 0.2 if expectancy > 0.5 else 0.1
                                    scale_lot = round((base_lot * scale_ratio) / v_step) * v_step
                                    scale_lot = max(scale_lot, min_lot)
                                    
                                    res = self.bridges.execute_order(current_symbol, target_pos['side'], scale_lot, unit_id=self.unit_id)
                                    if res:
                                        # Track Delta (Expectancy Improvement)
                                        self.forensics.log_event(self.unit_id, "REINFORCEMENT", f"{current_symbol} Layer {len(active_symbol_pos)+1} | Lot: {scale_lot}")
                                        
                                        if self.unit_id not in self.dna: self.dna[self.unit_id] = {}
                                        self.dna[self.unit_id]["LAST_SCALE"] = time.time()
                                        with open(self.dna_path, 'w') as f: json.dump(self.dna, f, indent=4)

                            except Exception as harvester_err:
                                self.logger.error(f" !! [HARVESTER_ERR] {self.unit_id} scale-in failed: {harvester_err}")
                        
                        continue

                    # 6. EXECUTION STRIKE
                    side = "BUY" if bias == "BULLISH" else "SELL"
                    if bias == "NEUTRAL": continue 
                    
                    # 6. EMPIRICAL OPTIMIZATION (Context-Aware v2.0)
                    from optimizer import SovereignOptimizer
                    optimizer = SovereignOptimizer(self.bridges)
                    best_sl_mult, best_tp_mult = optimizer.optimize_targets(symbol, price, atr, side, er=er)
                    
                    # Capture Market Context for Learning
                    from datetime import datetime
                    utc_hour = datetime.utcnow().hour
                    session = "ASIA" if 0 <= utc_hour < 8 else "LONDON" if 8 <= utc_hour < 15 else "NEW_YORK"
                    
                    info = mt5.symbol_info(symbol)
                    spread_val = (info.spread * info.point) if info else 0
                    spread_ratio = round(spread_val / atr, 4) if atr > 0 else 0
                    
                    # REQUEST SOVEREIGN LOT & TARGETS
                    allowed, lot_or_reason = vault.pre_flight_check(self.unit_id, symbol, side, 0, price, forensics=self.forensics)
                    
                    if allowed:
                        lot = lot_or_reason
                        # Use Empirical Multipliers from the Optimizer
                        sl, tp = vault.get_sl_tp(self.unit_id, symbol, side, price, atr, er=er) # ER still used for regime bias
                        
                        # OVERRIDE with Empirical Targets
                        sl_dist = atr * best_sl_mult
                        tp_dist = atr * best_tp_mult
                        if side == "BUY":
                            sl, tp = price - sl_dist, price + tp_dist
                        else:
                            sl, tp = price + sl_dist, price - tp_dist
                        
                        self.logger.info(f" >> [EMPIRICAL] Using Optimized Targets: SL {best_sl_mult}x | TP {best_tp_mult}x")
                        
                        # 6. MASTER SAFETY WRAPPER (Final Forensic Gate)
                        from safety import IronSafety
                        safety = IronSafety()
                        
                        # A. Dead Man Switch (Fail-Closed)
                        is_healthy, health_reason = safety.system_integrity_audit()
                        if not is_healthy:
                            self.logger.error(f" !! [FAIL_CLOSED] System Stand-Down: {health_reason}")
                            time.sleep(60) # Stand down for a minute
                            continue

                        # B. Global Exposure Check
                        active_pos = self.bridges.get_active_positions()
                        
                        # C. SYMBOL LOCK (Anti-Spam)
                        symbol_positions = [p for p in active_pos if p.get('symbol') == symbol]
                        if len(symbol_positions) > 0:
                            self.logger.warning(f" !! [POSITION_LOCK] {symbol} already has an active strike. Aborting.")
                            continue

                        safe_to_strike, global_reason = self.safety.global_exposure_audit(active_pos)
                        if not safe_to_strike:
                            self.logger.warning(f" !! [SAFETY_BLOCK] Global Limit: {global_reason}")
                            continue
                            
                        # B. Pre-Flight Unit Audit
                        import MetaTrader5 as mt5
                        tick = mt5.symbol_info_tick(symbol)
                        spread = (tick.ask - tick.bid) if tick else 0
                        
                        safe_to_fire, safety_reason = self.safety.pre_flight_audit(self.unit_id, symbol, side, lot, price, atr, spread)
                        
                        if not safe_to_fire:
                            self.logger.error(f" !! [SAFETY_ABORT] {symbol}: {safety_reason}")
                            continue

                        # 7. PRE-FLIGHT LOGGING (Persistence Guard)
                        self.forensics.log_trade(self.unit_id, symbol, side, lot, price, sl, tp, status="PENDING", 
                                                 sl_mult=best_sl_mult, tp_mult=best_tp_mult, er=er,
                                                 atr=atr, spread=spread_ratio, session=session)
                        
                        # 8. ARCHIVE ENTRY PRICE TO DNA (For UI Visibility)
                        try:
                            with open("core_v3/dna.json", "r") as f:
                                dna_data = json.load(f)
                            if self.unit_id not in dna_data: dna_data[self.unit_id] = {}
                            dna_data[self.unit_id]["LAST_ENTRY"] = price
                            with open("core_v3/dna.json", "w") as f:
                                json.dump(dna_data, f, indent=4)
                        except Exception as e:
                            self.logger.error(f" !! [DNA_ERR] Failed to archive entry price: {e}")

                        # 9. EXECUTION STRIKE (WITH REAL-MONEY FIRELOCK)
                        is_demo = account.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO
                        
                        # --- STAGGERED ATTACK (Anti-Collision) ---
                        import random
                        time.sleep(random.random() * 2) 

                        if not is_demo:
                            self.logger.info(f" >> [FIRELOCK] Real Account Detected. Switching to SIGNAL-ONLY mode.")
                            result = True # Simulate success to trigger signal relay
                        else:
                            self.logger.info(f" >> [{self.unit_id}_STRIKE] Safety Verified. Executing {side} {symbol} @ {price} | LOT: {lot} | SL: {sl} | TP: {tp}")
                            result = self.bridges.execute_order(symbol, side, lot, sl=sl, tp=tp, unit_id=self.unit_id)
                                
                        # --- SOVEREIGN CO-PILOT SIGNAL (ALWAYS RELAY IF SAFETY PASS) ---
                        try:
                            # --- SIGNAL DEDUPLICATION ---
                            last_sig = self.signal_tracker.get(symbol)
                            now = time.time()
                            
                            # Only send if side changed OR it's been > 1 hour
                            should_send = False
                            if not last_sig:
                                should_send = True
                            elif last_sig['side'] != side:
                                should_send = True
                            elif (now - last_sig['time']) > 3600: # 1 Hour Cooldown
                                should_send = True
                            
                            if should_send:
                                from signal_commander import SignalCommander
                                sc = SignalCommander()
                                # Signal use 0.01 lot as guided by the commander for $100 plan
                                sc.send_signal(symbol, side, price, sl, tp, er, lot=0.01, reason="Elite Unit Strike")
                                self.logger.info(f" >> [RELAY] Signal relayed to Telegram.")
                                self.signal_tracker[symbol] = {'side': side, 'price': price, 'time': now}
                                self._save_tracker()
                            else:
                                self.logger.info(f" >> [DEDUPLICATION] {symbol} {side} signal suppressed (Duplicate).")
                                
                        except Exception as e:
                            self.logger.error(f" !! [SIGNAL_ERR] Failed to relay strike: {e}")

                        if result:
                            if is_demo:
                                self.logger.info(f" >> [SUCCESS] {symbol} {side} order completed.")
                                self.forensics.log_trade(self.unit_id, symbol, side, lot, price, sl, tp, 
                                                         status="CLOSED" if "USDT" in symbol else "LIVE", 
                                                         sl_mult=best_sl_mult, tp_mult=best_tp_mult, er=er,
                                                         atr=atr, spread=spread_ratio, session=session)
                        else:
                            self.logger.error(f" >> [FAILED] {symbol} {side} execution failed on Trial account.")
                            self.forensics.log_trade(self.unit_id, symbol, side, lot, price, sl, tp, 
                                                     status="FAILED", sl_mult=best_sl_mult, tp_mult=best_tp_mult, er=er,
                                                     atr=atr, spread=spread_ratio, session=session)
                    else:
                        reason = lot_or_reason
                        self.logger.warning(f" !! [VAULT_BLOCK] {symbol}: {reason}")
                
                
                time.sleep(30) # SI v3.5: Hyper-Slow Pulse
                
            except Exception as e:
                self.logger.error(f"CORE_LOOP_EXCEPTION: {e}")
                time.sleep(5)

if __name__ == "__main__":
    import sys
    unit_id = sys.argv[1] if len(sys.argv) > 1 else "ALPHA"
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_path = os.path.join(base_dir, "secrets.json")
    db_path = os.path.join(base_dir, "iron_core.db")
    
    engine = IronEngine(secrets_path, unit_id=unit_id)
    engine.forensics = IronForensics(db_path=db_path)
    engine.run()
