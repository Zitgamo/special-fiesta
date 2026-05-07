import pandas as pd
import numpy as np
import MetaTrader5 as mt5
import json
import os

class SovereignOptimizer:
    """
    The Empirical Engine.
    Replaces magic numbers with real-time backtest results.
    """
    def __init__(self, bridges=None):
        self.bridges = bridges

    def optimize_targets(self, symbol, current_price, atr, side, lookback_bars=200, er=0.5):
        """
        Runs a mini-backtest on the last X bars to find the optimal SL/TP Multipliers.
        Integrates historical hints for a 'Hybrid Learning' approach.
        """
        # 0. Check Historical Database for Hints (Experience Overlay)
        from forensics import IronForensics
        forensics = IronForensics()
        hint = forensics.get_optimal_hint(symbol, er)
        if hint:
            best_sl, best_tp = hint
            # SAFETY OVERRIDE: Ensure historical hints never return negative or zero multipliers
            best_sl = max(0.1, abs(best_sl))
            best_tp = max(0.1, abs(best_tp))
            print(f" >> [LEARNING_OVERLAY] Found historical best for {symbol} @ ER {er}: SL {best_sl}x | TP {best_tp}x")
            return best_sl, best_tp

        # 1. Fetch High-Fidelity Data
        if "USDT" in symbol:
             # Fallback for crypto (Binance backtesting requires more logic, using macro-heuristic for now)
             return 1.5, 3.0
             
        rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, lookback_bars)
        if rates is None or len(rates) < 50:
            return 1.5, 3.0 # Fallback to safe defaults
            
        df = pd.DataFrame(rates)
        
        # 2. Define Parameter Grid (Adaptive based on Regime)
        if er < 0.3: # RANGING/CHOP
            sl_options = [0.8, 1.0, 1.2, 1.5]
            tp_options = [1.5, 2.0, 2.5]
            regime = "RANGE"
        else: # TRENDING
            sl_options = [1.5, 2.0, 2.5]
            tp_options = [3.0, 4.0, 5.0, 6.0]
            regime = "TREND"
            
        best_expectancy = -999
        best_sl = 1.2 if regime == "RANGE" else 1.5
        best_tp = 2.0 if regime == "RANGE" else 3.5
        
        # 3. Simulation Loop
        for sl_mult in sl_options:
            for tp_mult in tp_options:
                expectancy = self._simulate(df, sl_mult * atr, tp_mult * atr, side)
                if expectancy > best_expectancy:
                    best_expectancy = expectancy
                    best_sl = sl_mult
                    best_tp = tp_mult
                    
        print(f" >> [OPTIMIZER] Regime: {regime} | Best Match: {best_sl}x / {best_tp}x (Exp: {best_expectancy:.4f})")
        return best_sl, best_tp

    def suggest_global_shift(self):
        """
        Analyzes the last 100 trades to see if the Global DNA multipliers 
        need a 'System-Wide' shift.
        """
        try:
            import sqlite3
            db_path = os.path.join(os.getcwd(), "core_v3", "iron_core.db")
            conn = sqlite3.connect(db_path)
            # Find the most successful SL/TP combinations in the current regime
            query = '''
                SELECT sl_mult, tp_mult, AVG(outcome_pnl) as expectancy
                FROM empirical_learning
                GROUP BY sl_mult, tp_mult
                HAVING COUNT(*) > 5
                ORDER BY expectancy DESC
                LIMIT 1
            '''
            df_perf = pd.read_sql_query(query, conn)
            conn.close()
            
            if not df_perf.empty:
                best = df_perf.iloc[0]
                return best['sl_mult'], best['tp_mult'], best['expectancy']
        except: pass
        return None

    def _simulate(self, df, sl_dist, tp_dist, side):
        """
        Fast Vectorized Simulation of the last N bars.
        """
        pnl_accum = 0
        strikes = 0
        
        # Simple walk-forward simulation
        for i in range(0, len(df) - 20, 2): # Step 2 for speed
            entry_price = df.iloc[i]['close']
            if side == "BUY":
                sl = entry_price - sl_dist
                tp = entry_price + tp_dist
            else:
                sl = entry_price + sl_dist
                tp = entry_price - tp_dist
                
            # Check window for exit (next 20 bars)
            window = df.iloc[i+1:i+21] 
            
            for _, bar in window.iterrows():
                if side == "BUY":
                    if bar['low'] <= sl: 
                        pnl_accum -= sl_dist
                        strikes += 1
                        break
                    if bar['high'] >= tp:
                        pnl_accum += tp_dist
                        strikes += 1
                        break
                else:
                    if bar['high'] >= sl:
                        pnl_accum -= sl_dist
                        strikes += 1
                        break
                    if bar['low'] <= tp:
                        pnl_accum += tp_dist
                        strikes += 1
                        break
                        
        return pnl_accum / strikes if strikes > 0 else 0

if __name__ == "__main__":
    if mt5.initialize():
        opt = SovereignOptimizer()
        # Test optimization for Gold
        best_sl, best_tp = opt.optimize_targets("XAUUSD", 2300, 5, "BUY")
        print(f"RESULT: SL {best_sl}, TP {best_tp}")
