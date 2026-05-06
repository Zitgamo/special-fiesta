import os
import json
import logging

class IronBridges:
    """
    Unified Execution Bridge with Lazy-Loading Compression.
    """
    def __init__(self, secrets_path):
        self.logger = logging.getLogger("IronBridges")
        with open(secrets_path, 'r') as f:
            self.secrets = json.load(f)
        
        dna_path = os.path.join(os.path.dirname(secrets_path), "dna.json")
        try:
            with open(dna_path, 'r') as f:
                self.dna = json.load(f)
        except:
            self.dna = {"GLOBAL": {"BINANCE_LEVERAGE": 0}}
            
        self._binance = None
        self._mt5_initialized = False

    @property
    def binance(self):
        """Lazy-load CCXT only when needed."""
        if self._binance is None:
            try:
                import ccxt
                self._binance = ccxt.binance({
                    'apiKey': self.secrets.get('binance_api_key'),
                    'secret': self.secrets.get('binance_api_secret'),
                    'options': {'defaultType': 'future'}
                })
                # --- IMPERIAL LEVERAGE INJECTION (OPTIONAL) ---
                lev = self.dna.get("GLOBAL", {}).get("BINANCE_LEVERAGE", 0)
                if lev > 0:
                    try: self._binance.set_leverage(lev, "BTC/USDT")
                    except: pass
                    try: self._binance.set_leverage(lev, "ETH/USDT")
                    except: pass
                print("[BRIDGE] Binance API Handshake Successful.")
            except Exception as e:
                print(f"[BRIDGE_WARN] Binance Front Offline: {e}")
                self._binance = None
        return self._binance

    def _init_mt5(self):
        """Lazy-load MT5 only when needed."""
        if not self._mt5_initialized:
            import MetaTrader5 as mt5
            if mt5.initialize():
                self._mt5_initialized = True
                print("[BRIDGE] MT5 Neural Link Active.")
            else:
                print("[BRIDGE_ERR] MT5 Link Failed.")
        return self._mt5_initialized

    def get_price(self, symbol):
        if "USDT" in symbol:
            ticker = self.binance.fetch_ticker(symbol)
            return ticker['last']
        else:
            if not self._init_mt5(): return None
            import MetaTrader5 as mt5
            tick = mt5.symbol_info_tick(symbol)
            return tick.ask if tick else None

    def get_active_positions(self):
        """
        Unified Position Recon. Returns a standardized list of active deals.
        """
        all_pos = []
        # 1. MT5 Positions
        if self._init_mt5():
            import MetaTrader5 as mt5
            pos_list = mt5.positions_get()
            if pos_list:
                for p in pos_list:
                    all_pos.append({
                        "front": "MT5",
                        "ticket": p.ticket,
                        "symbol": p.symbol,
                        "side": "BUY" if p.type == 0 else "SELL",
                        "volume": p.volume,
                        "price_open": p.price_open,
                        "price_current": p.price_current,
                        "pnl": p.profit,
                        "sl": p.sl,
                        "tp": p.tp,
                        "magic": p.magic
                    })

        # 2. Binance Positions
        try:
            positions = self.binance.fetch_positions()
            for p in positions:
                vol = float(p['contracts'])
                if vol == 0: continue
                
                symbol_norm = p['symbol'].split(':')[0]
                
                # Fetch SL/TP for Binance (They are separate orders)
                sl_val, tp_val = 0, 0
                try:
                    orders = self.binance.fetch_open_orders(symbol_norm)
                    for o in orders:
                        if o['type'].upper() in ['STOP_MARKET', 'STOP']:
                            sl_val = float(o['stopPrice'] or o['price'])
                        if o['type'].upper() in ['TAKE_PROFIT_MARKET', 'LIMIT'] and o['side'].upper() != p['side'].upper():
                            tp_val = float(o['price'] or o['stopPrice'])
                except: pass

                all_pos.append({
                    "front": "BNC",
                    "ticket": symbol_norm,
                    "symbol": symbol_norm,
                    "side": p['side'].upper(),
                    "volume": abs(vol),
                    "price_open": float(p['entryPrice']),
                    "price_current": float(p['markPrice']),
                    "pnl": float(p['unrealizedPnl']),
                    "sl": sl_val,
                    "tp": tp_val,
                    "magic": 0
                })
        except Exception as e:
            self.logger.error(f" !! [RECON_ERR] Binance Front reconnaissance failed: {e}")
            
        return all_pos

    def _get_filling_mode(self, symbol):
        """Intelligently detects the correct filling mode for the broker/symbol."""
        import MetaTrader5 as mt5
        info = mt5.symbol_info(symbol)
        if not info: return mt5.ORDER_FILLING_FOK
        
        # bitmask check: 1=FOK, 2=IOC, 4=Return
        filling = info.filling_mode
        if filling == 1 or filling == 3: return mt5.ORDER_FILLING_FOK
        if filling == 2: return mt5.ORDER_FILLING_IOC
        return mt5.ORDER_FILLING_IOC # Fallback to IOC

    def close_partial(self, symbol, side, volume, ticket=None):
        """
        The 'Surgical Knife'. Closes a specific portion of an active deal.
        Includes 3-Strike Retry Logic for high-stakes combat.
        """
        if "USDT" in symbol:
            opp_side = "SELL" if side == "BUY" else "BUY"
            pos_side = "LONG" if side == "BUY" else "SHORT"
            for attempt in range(3):
                try:
                    return self.binance.create_order(symbol, "MARKET", opp_side, volume, params={'positionSide': pos_side})
                except Exception as e:
                    print(f" !!! [BNC_RETRY_{attempt}] Close failed: {e}")
            return None
        else:
            if not self._init_mt5(): return None
            import MetaTrader5 as mt5
            if not ticket: return None
            
            filling_mode = self._get_filling_mode(symbol)
            
            for attempt in range(3):
                tick = mt5.symbol_info_tick(symbol)
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": float(volume),
                    "type": mt5.ORDER_TYPE_SELL if side == "BUY" else mt5.ORDER_TYPE_BUY,
                    "position": ticket,
                    "price": tick.bid if side == "BUY" else tick.ask,
                    "deviation": 20,
                    "magic": 202605,
                    "comment": f"SHAVE_P{attempt}",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": filling_mode,
                }
                result = mt5.order_send(request)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    return result
                print(f" !!! [MT5_RETRY_{attempt}] Close failed: {result.comment} (Code: {result.retcode})")
            return None

    def execute_order(self, symbol, side, volume, sl=None, tp=None, order_type="MARKET", unit_id="ALPHA"):
        """
        Unified Execution Strike with Intelligent Retry.
        """
        import time
        unit_code = unit_id[0] if unit_id else "X"
        if "USDT" in symbol:
            for attempt in range(3):
                try:
                    # Dynamic Leverage Strike
                    lev = self.dna.get("GLOBAL", {}).get("BINANCE_LEVERAGE", 0)
                    if lev > 0:
                        try: self.binance.set_leverage(lev, symbol)
                        except: pass
                    
                    params = {'positionSide': 'LONG' if side.upper() == 'BUY' else 'SHORT'}
                    # Use unit_id in newClientOrderId for Binance
                    params['newClientOrderId'] = f"STRIKE_{unit_code}{int(time.time())}"
                    if sl: params['stopLoss'] = sl
                    if tp: params['takeProfit'] = tp
                    return self.binance.create_order(symbol, order_type, side.upper(), float(volume), params=params)
                except Exception as e:
                    self.logger.error(f" !!! [BNC_RETRY_{attempt}] {symbol} Order failed: {e}")
            return None
        else:
            # SAFETY CHECK: Prevent Crypto on MT5
            crypto_keywords = ["BTC", "ETH", "ADA", "SOL", "FIL", "DOGE", "XRP", "LTC", "DOT"]
            if any(k in symbol.upper() for k in crypto_keywords):
                print(f" !! [SAFETY_ABORT] Crypto strike blocked on MT5: {symbol}")
                return None
                
            if not self._init_mt5(): return None
            import MetaTrader5 as mt5
            
            filling_mode = self._get_filling_mode(symbol)
            
            for attempt in range(3):
                tick = mt5.symbol_info_tick(symbol)
                if not tick: continue
                
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": float(volume),
                    "type": mt5.ORDER_TYPE_BUY if side.upper() == "BUY" else mt5.ORDER_TYPE_SELL,
                    "price": tick.ask if side.upper() == "BUY" else tick.bid,
                    "sl": float(sl) if sl else 0.0,
                    "tp": float(tp) if tp else 0.0,
                    "deviation": 20,
                    "magic": 202605,
                    "comment": f"STRIKE_{unit_code}{attempt}",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": filling_mode,
                }
                result = mt5.order_send(request)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    return result
                
                error_msg = f" !!! [MT5_RETRY_{attempt}] Order failed: {result.comment} (Code: {result.retcode})"
                print(error_msg)
                self.logger.error(error_msg)
            return None
