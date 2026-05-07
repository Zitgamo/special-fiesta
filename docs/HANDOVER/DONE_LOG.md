m# 🦅 PROJECT MANIFEST: SOVEREIGN COMMANDER (v10.0)
**DATE:** 2026-05-05 | **STATUS:** OPERATIONAL / CO-PILOT ACTIVE | **EQUITY:** $931.11 (BNC) / $463k (Trial)

## 🛡️ THE ARCHITECTURE (SQL CORE v6.0)
- **Single Source of Truth**: `iron_core.db` (Local SQLite).
- **Hardening**: WAL Mode + v6.0 Retry Shield + **Silent Terminal Protocol**.
- **Primary Tables**:
  - `live_orders`: Current engagements (Symbol, Side, Entry, PnL, Exchange).
  - `squad_status`: Unit heartbeats (Rank, XP, State, Last Seen).
  - `equity_history`: Performance tracking for the ROI Heatmap.

## ⚔️ ACTIVE SQUAD (SQUADRON-01)
1. **ALPHA-ADOPTED (7 Units)**: 
   - **Front**: Exness (MT5). 
   - **Strikes**: XAUGBP, US30, XAGUSD, DE30, GBPUSD, XAUUSD.
   - **State**: ADOPTED | Total PnL: Monitoring.
2. **Vanguard (V-01-LIVE)**: 
   - **State**: ATTACKING | PnL: +$46.75 | Identity: `RECOV_V-01-LIVE_xxxx`.
3. **Harvester (S-04-LIVE)**:
   - **State**: ATTACKING | Entry: $78,289.60 | Identity: `RECOV_S-04-LIVE_xxxx`.
4. **Grid Sniper (G-01-LIVE)**: Monitoring BTC grid layers.

## 🛰️ SHADOW-LINK v8.5 (REMOTE OVERWATCH)
- **Telegram Bot**: WAVERIDER (Token: `8734076950:AAHajuNZ3YnIDuxVAVtOEzHyATZFXqLmpmo`).
- **Pure Proxy Mode**: Local AI (Ollama) MUTED. Bridge acts as a raw radio link.
- **Ghost Relay (v8.8)**: Actively intercepts mobile chat and injects directly into Antigravity IDE (Sector-Lock: Lower-Right).
- **Signal-Only Protocol**: Real account is traded MANUALLY via Telegram strikes. Bot executes ONLY on Trial.
- **Signal Anti-Spam**: Deduplication active (1-hour cooldown per side/symbol).
- **Outbox Pipeline**: `tele_outbox.txt` handles AI-to-Mobile communication.

## 🎖️ VETERANCY & XP SYSTEM
- **Logic**: XP gained per profitable strike (calculated on retreat).
- **Scale**: Recruit (Rank 0) -> Veteran (Rank 1) -> Elite (Rank 2).
- **Current Goal**: V-01 and S-04 are accumulating XP for Rank-Up.

## 🗺️ TACTICAL MAP v9.0 (DASHBOARD)
- **URL**: `http://localhost:8501` (Streamlit).
- **Fidelity**: Strictly filters for `ENGAGED` orders only (No historical ghosts).
- **Features**: Live Engagement Terminal, ROI Heatmap, Veterancy Roster.

## 📝 NEXT-STEPS / HANDOVER
- [x] **Silent Terminal Protocol**: Purged all vocal interaction modules (v10.0).
- [x] **Logic Stabilization**: Fixed critical `NameError` in `vault_v2.py` (balance bug).
- [x] **Sentinel Persistence**: Iron Sentinel v3.0 active and resurrecting fleet.
- [x] **Co-Pilot Deployment**: Abandoned real account handshake. Bot now running on Trial with Telegram relay.

**COMMANDER INTENT:** "Transitioned to Sovereign Co-Pilot protocol. Fleet is patrolling on Trial account. Tactical strikes are being relayed via Telegram for manual Real account execution."
**SYSTEM NOTE:** System is autonomous. Ghost-Relay is active. Remote-Proxy is listening.
