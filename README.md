# 🛰️ Iron Commander Elite (v3.5)

**Iron Commander Elite** is a sovereign, autonomous trading ecosystem inspired by Real-Time Strategy (RTS) mechanics. It orchestrates multiple independent trading units (Soldiers) using a central risk/logic controller (Master) via a hardened forensic ledger.

## 🏛️ Project Architecture: The Trinity Fronts
The system operates across three distinct tactical fronts:
1.  **Western Front (Exness/MT5):** Forex, Metals, and Indices. Managed by `ALPHA`, `OMEGA`, and `GAMMA` units.
2.  **Eastern Front (Binance):** High-volatility Cryptocurrencies.
3.  **Southern Front (VN30):** Alpha harvesting and paper-trading on Vietnam Index Futures.

## 📂 Directory Structure

| Directory | Purpose |
| :--- | :--- |
| [**`core_v3/`**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/core_v3) | The primary engine, orchestrator, and trading logic. |
| [**`nexus/`**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/nexus) | Tactical dashboards for real-time monitoring. |
| [**`03_DATA/`**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/03_DATA) | Persistent data storage and historical logs. |
| `logs/` | System-wide operational logs. |

## 🛠️ Key Components

### 1. The Master Orchestrator (`master.py`)
The central "General" that scans markets, detects regimes (Trending/Ranging), and dynamically allocates capital and assets to the frontline units.

### 2. The Iron Engines (`engine.py`)
The autonomous "Soldiers" that execute tactical strikes.
- **ALPHA:** Stability-focused, ranging logic.
- **OMEGA:** Aggressive, trend-following logic with layering protocol.
- **GAMMA:** Momentum and breakout specialist.

### 3. The Sentinel (`sentinel.py`)
A self-healing process guard that ensures 24/7 persistence, automatically restarting any crashed units and monitoring system health.

### 4. The Sovereign Nexus
A suite of high-fidelity HTML dashboards providing tactical transparency into fleet performance and market conditions.

## 📖 Essential Documentation
- [**Sovereign Bible**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/sovereign_bible.md): The core architectural mandate and trading philosophy.
- [**Master Plan**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/SOVEREIGN_MASTER_PLAN.md): The original design blueprint.
- [**Agent Protocol**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/AGENT_PROTOCOL_AND_TRACKER.md): Guidelines for AI interaction with the codebase.
- [**Manual Control Guide**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/MANUAL_CONTROL.md): How to start/stop the bot manually.

## 🚀 Quick Start
To launch the full sovereign fleet:
1. Ensure MT5 and Binance API keys are configured in `core_v3/secrets.json`.
2. Run the main launch script:
   ```powershell
   ./SOVEREIGN_REAL_LAUNCH.bat
   ```
3. Monitor the fleet via the [**Sovereign Nexus Dashboard**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/nexus/sovereign_nexus.html).

---
**Motto:** Data over Magic. Efficiency over Hope.
