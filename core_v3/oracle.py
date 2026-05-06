import json
import os
import time

class SovereignOracle:
    """
    Macro Intelligence Engine.
    Analyzes Global Bias and Sets the Market Regime.
    """
    def __init__(self, dna_path="core_v3/dna.json"):
        self.dna_path = dna_path

    def analyze_regime(self, bridges):
        """
        Scans Global Indices to determine the 'Global Tide'.
        """
        print(" >> [ORACLE] Analyzing Global Macro Regime...")
        try:
            # 1. FETCH MACRO VITALS (DXY, US10Y, VIX)
            dxy = bridges.get_price("USDLFX") # Proxy for Dollar
            gold = bridges.get_price("XAUUSD")
            vix = bridges.get_price("VIX") or 20 # Placeholder if not available
            
            bias = "NEUTRAL"
            if dxy and dxy > 100: bias = "USD_STRENGTH"
            if gold and gold > 2000: bias = "GOLD_MOMENTUM"
            
            # 2. UPDATE GLOBAL DNA
            with open(self.dna_path, 'r') as f:
                dna = json.load(f)
            
            dna["GLOBAL"]["REGIME"] = bias
            dna["GLOBAL"]["VIX_LEVEL"] = vix
            dna["GLOBAL"]["LAST_ORACLE_SCAN"] = time.ctime()
            
            with open(self.dna_path, 'w') as f:
                json.dump(dna, f, indent=4)
                
            print(f" >> [ORACLE] Regime Set: {bias} (VIX: {vix})")
            return bias
        except Exception as e:
            print(f" !! [ORACLE_ERR] {e}")
            return "NEUTRAL"

if __name__ == "__main__":
    # Test logic
    oracle = SovereignOracle()
    print("Oracle Logic Prepped.")
