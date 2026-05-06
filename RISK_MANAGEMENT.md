# 🛡️ Sovereign Risk Management (v3.5)

The Iron Commander Elite system employs a sophisticated, non-heuristic risk management protocol managed primarily by the [**`IronVault`**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/vault_v2.py).

## 🏛️ The Law of No Magic Numbers
Every strike (trade) must have its parameters derived from current market data, not hard-coded heuristics.

1.  **Dynamic Lot Sizing:** Lot sizes are calculated based on:
    - **Current Equity:** The available capital in the unit's virtual pool.
    - **ATR (Average True Range):** The current volatility of the asset.
    - **Risk Percentage:** Defined in the `NAV_RISK` protocol (0.5% - 1.0%).
2.  **Kelly Adjustment:** Risk is automatically scaled based on the unit's historical win rate and Reward/Risk ratio.
3.  **Veterancy Scaling:** Proven units (higher rank) are granted higher strike power (up to 2x).

## 🧬 Virtual Equity Isolation
The system divides the total account equity into virtual pools for each unit:
- **ALPHA:** Stability pool.
- **OMEGA:** Aggressive/Growth pool.
- **GAMMA:** Momentum pool.
This ensures that a drawdown in one unit does not immediately jeopardize the capital of others.

## 📉 Gradient Risk Protocol
The `Gradient Risk` mechanism monitors the global portfolio drawdown.
- **0% Drawdown:** 100% strike power.
- **20% Drawdown:** 0% strike power (Full Stand-down).
- Strike power decays linearly between these two points.

## ⚖️ Active Risk Governor
Once a position is live, the `Active Risk Governor` manages it autonomously using the **Sovereign Risk-Neutral Protocol (v3.4)**:

### 1. Relief Shave (Winner Side)
- When a trade reaches a High Water Mark (HWM) and then retraces, the system "shaves" (partially closes) 10% of the position.
- This banks "House Money" and reduces exposure during a potential reversal.

### 2. House Money Add (Loser Side)
- The system **NEVER** performs standard DCA on losing trades.
- It only adds to a position on a retest of support/resistance **IF** there is enough "House Money" banked from previous shaves.
- This ensures that scaling-in is funded by profits, not account principal.

### 🏹 Safe Handover (SL Sync)
The system continuously updates Stop Loss (SL) and Take Profit (TP) levels to adapt to changing volatility (ATR) and market regimes (Trending vs. Ranging).

---
**Protocol Motto:** Efficiency over Hope. Protect the Principal at all costs.
