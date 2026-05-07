from analytics import IronAnalytics
from optimizer import SovereignOptimizer
import MetaTrader5 as mt5
import pandas as pd

def alpha_scout():
    if not mt5.initialize():
        print(" !! MT5 INIT FAILED")
        return

    targets = ["US30", "XAUUSD", "EURUSD", "GBPUSD", "NAS100", "US500", "USDKGS"]
    results = []

    print("--- SOVEREIGN ALPHA SCOUT ---")
    for symbol in targets:
        er = IronAnalytics.get_efficiency_ratio(symbol)
        velocity = IronAnalytics.get_velocity(symbol)
        
        # Run Optimizer on Buy Side
        opt = SovereignOptimizer()
        sl_mult, tp_mult = opt.optimize_targets(symbol, 0, 10, "BUY")
        
        # Calculate a basic Alpha Score (ER * Velocity)
        alpha_score = er * velocity
        
        results.append({
            "Symbol": symbol,
            "ER": er,
            "Vel": velocity,
            "Alpha": round(alpha_score, 2),
            "Best_SL": sl_mult,
            "Best_TP": tp_mult
        })

    df = pd.DataFrame(results).sort_values(by="Alpha", ascending=False)
    print(df.to_string(index=False))

if __name__ == "__main__":
    alpha_scout()
