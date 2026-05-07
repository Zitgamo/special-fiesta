# 🛰️ Iron Commander Elite (v4.2.5)
## [Sovereign Autonomous Trading Ecosystem]

**Iron Commander Elite** is a high-integrity, modular trading system designed for autonomous multi-asset execution. It is built on a "Genetic DNA" model that self-optimizes based on market regimes.

---

## 📂 Project Structure

| Component | Path | Description |
| :--- | :--- | :--- |
| **Orchestrator** | [**`core_v3/`**](./core_v3) | The primary engine, analytics, and safety protocols. |
| **Interface** | [**`nexus/`**](./nexus) | Tactical HTML5 dashboards for real-time monitoring. |
| **Knowledge** | [**`docs/`**](./docs) | System architecture, protocols, and manuals. |
| **Data** | `03_DATA/` | Local database and persistent state (Git-ignored). |

## 🚀 Quick Start (Retail Deployment)

To launch your sovereign fleet:

1.  **Configure Secrets**:
    - Rename `core_v3/secrets.json.example` to `core_v3/secrets.json`.
    - Fill in your API keys (Binance, MT5, Telegram).
2.  **Environment Setup**:
    - Ensure Python 3.12+ is installed with `talib`, `pandas`, and `MetaTrader5`.
3.  **Launch**:
    - Run the main launch script: `./SOVEREIGN_REAL_LAUNCH.bat`.
4.  **Monitor**:
    - Open [**`nexus/sovereign_nexus.html`**](./nexus/sovereign_nexus.html) in any modern browser.

## 🛡️ Sovereign Security & Safety
- **Zero-Exposure**: API keys are never tracked in version control (enforced by `.gitignore`).
- **Emergency Kill-Switch**: Use [**`KILL_SWITCH.bat`**](./KILL_SWITCH.bat) to immediately freeze all trading processes.
- **Genetic Guardrails**: Built-in Drawdown and Exposure limits protect capital at the engine level.

## 🏛️ Documentation Index
- [**Master Index (Start Here)**](./docs/00_INDEX.md)
- [**User Manual**](./docs/USER_MANUAL_CONTROL.md)
- [**Release Protocol**](./docs/PROTOCOL/RELEASE_PROTOCOL.md)

---
**Status:** `STABLE // v4.2.5`
**Shipment Integrity:** `HARDENED`
**Commander:** *Zitgamo*
