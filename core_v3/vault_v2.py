import MetaTrader5 as mt5
import json
import os
import logging
import time
import analytics

class IronVault:
    def __init__(self, bridges=None, dna_path="dna.json"):
        self.dna_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), dna_path)
        self.dna = self._load_dna()
        self.bridges = bridges
        self.logger = logging.getLogger("IronVault")
        self.equity_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "virtual_equity.json")
        
        # --- SOVEREIGN PROTOCOL CONSTANTS (Line 13-15) ---
        self.NAV_RISK = {
            "ALPHA": 0.010, # 1.0%
            "OMEGA": 0.005, # 0.5%
            "GAMMA": 0.005  # 0.5%
        }
        
        self.virtual_pools = self._load_virtual_pools()

    def _load_dna(self):
        with open(self.dna_path, "r") as f:
            return json.load(f)

    def _load_virtual_pools(self):
        if os.path.exists(self.equity_path):
            try:
                with open(self.equity_path, "r") as f:
                    return json.load(f)
            except: pass
            
        # Initialization: Divide current total equity by 3
        acc = mt5.account_info()
        total = acc.equity if acc else 100.0
        pools = {
            "ALPHA": total / 3,
            "OMEGA": total / 3,
            "GAMMA": total / 3,
            "LAST_SYNC": time.time()
        }
        self._save_virtual_pools(pools)
        return pools

    def _save_virtual_pools(self, pools):
        with open(self.equity_path, "w") as f:
            json.dump(pools, f, indent=4)
            
    def update_pool_profit(self, unit_id, pnl_usd):
        """
        Settles a strike by adding/subtracting profit from the unit's virtual pool.
        """
        self.virtual_pools = self._load_virtual_pools()
        if unit_id in self.virtual_pools:
            self.virtual_pools[unit_id] += pnl_usd
            self.virtual_pools["LAST_SYNC"] = time.time()
            self._save_virtual_pools(self.virtual_pools)
            self.logger.info(f" >> [SETTLEMENT] {unit_id} virtual pool updated by ${pnl_usd:+.2f}")

    def get_gradient_risk(self):
        """
        Adjusts global strike power based on overall portfolio health.
        """
        try:
            acc = mt5.account_info()
            if not acc: return 1.0
            
            # Simple Linear Decay: 100% power at 0 DD, 0% power at 20% DD
            dd = (acc.balance - acc.equity) / acc.balance if acc.balance > 0 else 0
            risk_mult = max(0.0, 1.0 - (dd / 0.20))
            return round(risk_mult, 2)
        except: return 1.0

    def pre_flight_check(self, unit_id, symbol, side, volume, price, forensics=None):
        """
        SOVEREIGN PROTOCOL COMPLIANT (v3.0)
        Calculates Lot Size dynamically using the Law of No Magic Numbers.
        """
        grad_risk = self.get_gradient_risk()
        
        # 1. Multi-Front Equity Detection
        is_crypto = "USDT" in symbol
        if is_crypto and self.bridges:
            try:
                bal_data = self.bridges.binance.fetch_balance()
                current_balance = bal_data['total']['USDT']
            except: return False, "BINANCE_OFFLINE"
        else:
            # Protocol Isolation: Use Virtual Pool for MT5 Units
            current_balance = self.virtual_pools.get(unit_id, 0)
            if current_balance <= 0:
                # Fallback to global if pool is empty/uninitialized
                acc = mt5.account_info()
                if not acc: return False, "MT5_OFFLINE"
                current_balance = acc.equity / 3
                self.virtual_pools[unit_id] = current_balance
                self._save_virtual_pools(self.virtual_pools)

        # 2. Dynamic Volatility (ATR)
        atr_now = analytics.IronAnalytics.get_atr(symbol, self.bridges)
        if not atr_now: 
            # Protocol Fallback: 0.1% of price if ATR data is cold
            atr_now = price * 0.001

        # 3. Dynamic Win-Rate (Forensics)
        win_rate = 0.50
        if forensics:
            stats = forensics.get_unit_stats(unit_id)
            win_rate = stats.get("win_rate", 0.50)
        
        # 4. Reward/Risk (DNA)
        unit_dna = self.dna.get(unit_id, {"SL": 2.0, "TP": 4.0})
        rr = unit_dna["TP"] / unit_dna["SL"] if unit_dna["SL"] > 0 else 2.0
        
        # 5. The Dynamic Risk Formula (Strike Veteran Protocol)
        protocol_risk = self.NAV_RISK.get(unit_id, 0.005)
        kelly_adj = 1.0 # Default to Neutral
        veterancy_mult = 1.0
        
        if forensics:
            stats = forensics.get_unit_stats(unit_id)
            win_rate = stats.get("win_rate", 0.50)
            total_strikes = stats.get("total", 0) # Fixed from 'strikes'
            
            # A. Kelly Warm-up
            if total_strikes >= 10:
                kelly_adj = (win_rate * rr - (1 - win_rate)) / rr if rr > 0 else 1.0
                kelly_adj = max(0.5, min(2.0, kelly_adj)) # Clamp
            
            # B. Veterancy Scaling
            rank_data = forensics.get_unit_rank(unit_id)
            if rank_data['rank'] >= 1:
                veterancy_mult = 2.0
                self.logger.info(f" >> [VETERANCY] {unit_id} Rank {rank_data['rank']} detected. Applying 2x multiplier.")

        # Risk = Protocol_NAV * Kelly_Adjustment * Veterancy_Multiplier * Portfolio_Gradient
        risk_pct = protocol_risk * kelly_adj * veterancy_mult * grad_risk
        
        # 6. Lot Size Calculation (Law of No Magic Numbers)
        MAX_LOT = 0.05 # SOVEREIGN SAFETY CAP (Intended for Forex/Gold)
        sl_dist = atr_now * unit_dna["SL"]
        
        contract_size = 0 
        min_lot = 0.01
        volume_step = 0.01
        
        if not is_crypto:
            info = mt5.symbol_info(symbol)
            if info: 
                contract_size = info.trade_contract_size
                min_lot = info.volume_min
                volume_step = info.volume_step
            else:
                self.logger.error(f" !! [SAFETY_ABORT] Could not verify contract size for {symbol}. Blocking trade.")
                return False, "SYMBOL_INFO_MISSING"
        else:
            contract_size = 1.0 # Binance always 1.0
            min_lot = 0.001
            volume_step = 0.001
            
        if contract_size <= 0:
            self.logger.error(f" !! [SAFETY_ABORT] Invalid contract size ({contract_size}) for {symbol}. Blocking trade.")
            return False, "INVALID_CONTRACT_SIZE"
            
        risk_amount = current_balance * risk_pct
        
        # Calculate raw lot based on risk and SL distance
        if (sl_dist * contract_size) > 0:
            raw_lot = risk_amount / (sl_dist * contract_size)
        else:
            raw_lot = min_lot

        # Rounding according to Broker Step
        import math
        lot = round(raw_lot / volume_step) * volume_step
        lot = round(lot, 5) # Clean precision issues
        
        if lot < min_lot: 
            lot = min_lot
        
        # 7. SOVEREIGN SAFETY CAP (Smart Clamping)
        # We respect the 0.05 cap for most symbols, but allow the minimum if it's an Index (like JP225 min 1.0)
        if lot > MAX_LOT:
            if min_lot > MAX_LOT:
                # adaptive cap for Indices
                lot = min_lot
                self.logger.info(f" >> [VOLUME_ADAPTIVE] {symbol} requires min {min_lot}. Adjusting cap.")
            else:
                self.logger.warning(f" !! [SAFETY_CLAMP] Capping {lot} -> {MAX_LOT} for {symbol}")
                lot = MAX_LOT

        # 8. FINAL DOLLAR RISK AUDIT (Fail-Safe)
        # Ensure that even with min_lot, we aren't risking more than 3% of the account in one strike
        final_risk_usd = lot * sl_dist * contract_size
        max_allowed_risk_usd = current_balance * 0.03 # 3% Hard Limit
        
        if final_risk_usd > max_allowed_risk_usd:
            self.logger.error(f" !! [SAFETY_ABORT] {symbol}: Risk too high even at min lot (${final_risk_usd:.2f} > ${max_allowed_risk_usd:.2f})")
            return False, "RISK_TOO_HIGH"
        
        # Margin Check (Safety Floor)
        if is_crypto:
            lev = self.dna.get("GLOBAL", {}).get("BINANCE_LEVERAGE", 20)
            margin_required = (lot * price) / (lev if lev > 0 else 1)
            if margin_required > current_balance:
                self.logger.warning(f" !! [SAFETY_ABORT] {symbol}: INSUFFICIENT_MARGIN ({margin_required:.2f} > {current_balance:.2f})")
                return False, "INSUFFICIENT_MARGIN"

        # --- SOVEREIGN REAL-START SAFETY (Micro-Account Guard) ---
        if current_balance < 500:
            if lot > max(0.01, min_lot):
                self.logger.info(f" !! [REAL_START] Small Account detected (${current_balance:.2f}). Enforcing Safety Lot Cap.")
                lot = max(0.01, min_lot)

        self.logger.info(f"VAULT_PASS [{unit_id}]: {symbol} {lot} (Risk: {risk_pct*100:.3f}%, USD Risk: ${final_risk_usd:.2f})")
        return True, lot

    def get_sl_tp(self, unit_id, symbol, side, price, atr, er=0.5):
        dna = self.dna.get(unit_id, {"SL": 1.5, "TP": 3.0})
        sl_mult = dna.get("SL", 1.5)
        tp_mult = dna.get("TP", 3.0)
        
        # --- REGIME ADAPTIVE SCALING (ER-DRIVEN) ---
        if er > 0.6: # Trending Regime
            self.logger.info(f" >> [REGIME] Trending detected (ER: {er}). Stretching TP for capture.")
            tp_mult *= 1.5
            sl_mult *= 0.8
        elif er < 0.35: # Ranging Regime
            self.logger.info(f" >> [REGIME] Ranging detected (ER: {er}). Tightening targets for scalp.")
            tp_mult *= 0.6
            sl_mult *= 1.2
            
        sl_dist = atr * sl_mult
        tp_dist = atr * tp_mult
        
        if side == "BUY":
            sl = price - sl_dist
            tp = price + tp_dist
            # Safety floor: SL cannot go below 0 or below 1% of price for micro pairs
            if sl <= 0 or sl < price * 0.01:
                sl = max(0.00001, price * 0.99)  # Minimum 1% below price
                self.logger.warning(f" !! [SAFETY_FLOOR] SL clamped to {sl} (was negative/too low)")
        else:
            sl = price + sl_dist
            tp = price - tp_dist
            # Safety floor: SELL SL cannot exceed 101% of price
            if sl > price * 1.01:
                sl = price * 1.01
                self.logger.warning(f" !! [SAFETY_FLOOR] SL clamped to {sl} (was too high)")
            
        return round(sl, 5), round(tp, 5)

    def active_risk_governor(self, bridges, engine=None):
        positions = bridges.get_active_positions()

        tracker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pos_tracker.json")
        tracker = {}
        if os.path.exists(tracker_path):
            try:
                with open(tracker_path, "r") as f:
                    tracker = json.load(f)
            except: tracker = {}

        for pos in positions:
            try:
                symbol = pos['symbol']
                ticket = str(pos['ticket'])
                side = pos['side']
                pnl = pos['pnl']
                volume = pos['volume']
                unit_id = self._identify_unit(pos)

                # --- 1. AUTONOMOUS MILKING (HWM SHAVING) ---
                self.autonomous_shave(ticket, symbol, side, volume, pnl, unit_id, bridges, tracker)
                
                # --- 2. SAFE HANDOVER (SL SYNC) ---
                atr = analytics.IronAnalytics.get_atr(symbol, bridges)
                if not atr: continue
                
                new_sl, new_tp = self.get_sl_tp(unit_id, symbol, side, pos['price_open'], atr)
                
                # Only sync if better for the user
                should_sync = False
                if side == "BUY":
                    if new_sl > pos['sl'] and new_sl < pos['price_current']: should_sync = True
                else:
                    if new_sl < pos['sl'] and new_sl > pos['price_current']: should_sync = True
                
                if should_sync:
                    self.logger.info(f" >> [SAFE_HANDOVER] Syncing {symbol} SL to {new_sl}")
                    self._modify_mt5_sl(ticket, new_sl, new_tp)

            except Exception as e:
                self.logger.error(f" !! [VAULT_GOVERNOR_ERR] {e}")

    def autonomous_shave(self, ticket, symbol, side, volume, pnl, unit_id, bridges, tracker):
        """
        Sovereign Risk-Neutral Protocol (v3.4):
        1. Relief Shave: Trim profit at HWM relief (Winner side).
        2. House Money Add: Add at LWM retest ONLY if banked profit > 0 (Loser side).
        """
        try:
            # 1. Initialize Tracker Entry
            if ticket not in tracker:
                tracker[ticket] = {
                    "hwm": pnl, "hwm_state": "INITIAL",
                    "lwm": pnl, "lwm_state": "INITIAL",
                    "banked": 0.0
                }
                self._save_tracker(tracker)

            data = tracker[ticket]
            dna = self.dna.get(unit_id, {}).get("ACTIVE_RISK", {})
            shave_ratio = dna.get("SHAVE_RATIO", 0.1)
            add_ratio = dna.get("SHAVE_RATIO", 0.1) # Default to same ratio for adding
            min_threshold = 1.0

            # --- A. WINNER SIDE (RELIEF SHAVE) ---
            if data["hwm_state"] == "INITIAL":
                if pnl > data["hwm"]:
                    data["hwm"] = pnl
                    if data["hwm"] >= min_threshold:
                        data["hwm_state"] = "HWM_SET"
                        self._save_tracker(tracker)
            elif data["hwm_state"] == "HWM_SET":
                if pnl > data["hwm"]:
                    data["hwm"] = pnl
                    self._save_tracker(tracker)
                elif pnl <= 0.1: # Retraced to entry
                    data["hwm_state"] = "RETRACED"
                    self._save_tracker(tracker)
            elif data["hwm_state"] == "RETRACED":
                if pnl >= data["hwm"]:
                    shave_vol = round(volume * shave_ratio, 2)
                    if shave_vol >= 0.01:
                        self.logger.info(f" >> [RELIEF_SHAVE] {symbol} (Winner) second chance @ ${pnl:.2f}. Trimming {shave_vol}...")
                        res = bridges.close_partial(symbol, side, shave_vol, ticket=int(ticket) if "USDT" not in symbol else None)
                        if res:
                            data["hwm_state"] = "TRIMMED"
                            data["banked"] += (pnl * shave_ratio)
                            self._save_tracker(tracker)

            # --- B. LOSER SIDE (HOUSE MONEY ADD) ---
            if data["lwm_state"] == "INITIAL":
                if pnl < data["lwm"]:
                    data["lwm"] = pnl
                    if data["lwm"] <= -min_threshold:
                        data["lwm_state"] = "LWM_SET"
                        self._save_tracker(tracker)
            elif data["lwm_state"] == "LWM_SET":
                if pnl < data["lwm"]:
                    data["lwm"] = pnl
                    self._save_tracker(tracker)
                elif pnl >= -0.1: # Recovered to entry
                    data["lwm_state"] = "RECOVERED"
                    self.logger.info(f" >> [RECOVERY_WATCH] {symbol} recovered from -${abs(data['lwm']):.2f}. Monitoring support retest...")
                    self._save_tracker(tracker)
            elif data["lwm_state"] == "RECOVERED":
                if pnl <= data["lwm"]:
                    # CRITICAL CONDITION: Only add if we have House Money (Banked Profit)
                    if data["banked"] > 0:
                        add_vol = round(volume * add_ratio, 2)
                        if add_vol >= 0.01:
                            self.logger.info(f" >> [HOUSE_MONEY_ADD] {symbol} retesting support @ -${abs(pnl):.2f}. Adding {add_vol} using banked ${data['banked']:.2f}...")
                            # To add back, we execute a new STRIKE on the same side
                            res = bridges.execute_order(symbol, side, add_vol, unit_id=unit_id)
                            if res:
                                data["lwm_state"] = "ADDED"
                                self._save_tracker(tracker)
                    else:
                        self.logger.info(f" >> [DCA_BLOCKED] {symbol} retesting support but NO HOUSE MONEY banked. Aborting add.")
                        data["lwm_state"] = "BLOCKED" # Don't check again for this retest
                        self._save_tracker(tracker)

        except Exception as e:
            self.logger.error(f" !! [RISK_NEUTRAL_ERR] {e}")

    def _save_tracker(self, tracker):
        tracker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pos_tracker.json")
        with open(tracker_path, "w") as f:
            json.dump(tracker, f, indent=4)

    def _identify_unit(self, pos):
        magic = pos.get('magic', 0)
        if magic == 202605: return "ALPHA" # Default for v3 strikes
        # Logic to extract unit from comment if possible
        return "OMEGA" # Fallback

    def _modify_mt5_sl(self, ticket, sl, tp):
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": int(ticket),
            "sl": float(sl),
            "tp": float(tp)
        }
        mt5.order_send(request)
