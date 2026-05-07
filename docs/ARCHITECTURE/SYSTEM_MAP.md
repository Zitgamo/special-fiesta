# 🗺️ SOVEREIGN SYSTEM MAP
## [The Retail Core v4.2.5]

This map provides a high-level overview of the Sovereign Elite infrastructure for deployment and monitoring.

---

## 🏛️ 1. OPERATIONAL ROOT
- [**`SOVEREIGN_REAL_LAUNCH.bat`**](../../SOVEREIGN_REAL_LAUNCH.bat): The primary entry point for the fleet.
- [**`KILL_SWITCH.bat`**](../../KILL_SWITCH.bat): Emergency global freeze and process termination.
- [**`janitor.py`**](../../janitor.py): Autonomous background maintenance and DB optimization.

## 🧠 2. THE ENGINE CORE (`core_v3/`)
- **`master.py`**: The central orchestrator. Handles startup and multi-unit synchronization.
- **`sentinel.py`**: High-availability process watchdog. Ensures 24/7 uptime.
- **`fleet_report.py`**: Integrated Telegram telemetry engine (SSS + Council).
- **`engine.py`**: The tactical execution module for all units (Alpha, Omega, Gamma).
- **`analytics.py`**: Real-time market regime, bias, and efficiency ratio calculation.
- **`safety.py`**: Implements global exposure limits and pre-flight risk checks.

## 📊 3. TACTICAL INTERFACE (`nexus/`)
- [**`sovereign_nexus.html`**](../../nexus/sovereign_nexus.html): The Master Dashboard for total fleet visibility.
- [**`southern_command.html`**](../../nexus/southern_command.html): Dedicated UI for VN30F1M index trading.
- [**`elite_report.html`**](../../nexus/elite_report.html): Detailed PnL and trade forensics view.

## 🗄️ 4. DATA & STATE (`03_DATA/`)
- **`iron_dna.json`**: Dynamic risk and execution parameters for all active units.
- **`iron_core.db`**: The unified SQLite ledger for all trade history and state snapshots.

---
**Status:** `READY FOR DEPLOYMENT`
**Integrity:** `CERTIFIED`
