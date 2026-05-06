# ⚙️ Core v3: The Sovereign Engine

This directory contains the primary logic, orchestration, and execution modules for the Iron Commander Elite trading system.

## 🗂️ Core Components

### 🧠 Orchestration & Intelligence
- **[`master.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/master.py):** The central brain. Handles market scanning, regime detection, DNA mutation, and capital allocation.
- **[`engine.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/engine.py):** The tactical execution engine. Processes signals, audits risk, and executes trades on MT5 and Binance.
- **[`oracle.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/oracle.py):** Provides predictive insights and data streams for decision-making.
- **[`optimizer.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/optimizer.py):** Performs 200-bar mini-backtests before every strike to ensure regime-adaptive parameters.

### 🛡️ Safety & Persistence
- **[`sentinel.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/sentinel.py):** Self-healing monitor that maintains process uptime.
- **[`safety.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/safety.py):** Implements global exposure limits, "Dead Man Switches," and pre-flight safety audits.
- **[`vault_v2.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/vault_v2.py):** Manages capital protection, profit shaving, and dynamic lot sizing.

### 📊 Data & Forensics
- **[`forensics.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/forensics.py):** The forensic ledger. Records every trade event, snapshot, and mutation in `iron_core.db`.
- **[`analytics.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/analytics.py):** Calculates session bias, Efficiency Ratio (ER), ATR, and momentum velocity.
- **[`iron_core.db`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/iron_core.db):** The SQLite single source of truth for the entire system.

### 🛰️ Connectivity
- **[`bridges.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/bridges.py):** Unified API bridge for MT5 and Binance.
- **[`ghost_comm.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/ghost_comm.py):** Telegram integration for remote command and real-time signal relay.
- **[`nexus_bridge.py`](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3/nexus_bridge.py):** Connects the backend engine to the HTML dashboards.

## 🧬 Data Structures
- **`dna.json`:** Stores the evolved parameters (SL/TP multipliers, Lot sizes) for each unit.
- **`squadron.json`:** Defines which assets are assigned to which unit based on the latest market scan.
- **`secrets.json`:** (Sensitive) Contains API credentials and account details.

## 🛠️ Operational Workflow
1.  **Orchestration:** `master.py` scans the market and updates `squadron.json`.
2.  **Deployment:** `sentinel.py` launches the required `engine.py` instances (ALPHA, OMEGA, GAMMA).
3.  **Execution:** Each engine performs a local scan -> analytics check -> pre-strike optimization -> safety audit -> execution.
4.  **Learning:** `master.py` periodically reviews performance in `iron_core.db` and mutates the `dna.json` to adapt to changing market conditions.

---
**Warning:** This core interacts with real-money accounts. Always verify `is_demo` status in logs before full deployment.
