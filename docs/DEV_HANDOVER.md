**Handover — IRON COMMANDER ELITE**

- **Date:** 2026-05-06
- **Prepared by:** Automated agent

**Status Summary**
- `core_v3`: Demo branch — RUNNING (engines ALPHA/OMEGA/GAMMA active). HTML UI (`nexus/sovereign_nexus.html`) is live and fed by `core_v3/nexus_bridge.py` on `http://127.0.0.1:5050`.
- `core_real`: Live branch — NOT launched (files `core_real/engine.py` and `core_real/vault_v2.py` were empty). Integrity check prevents auto-start.
- Maintenance: `janitor.py` in repo root performs daily cleanup; schedule with `JANITOR_SETUP.bat` (run as Admin).

**What I changed (May 6, 2026)**
- Removed legacy Streamlit UI (`tactical_map.py`) and references in `commander_control.py`.
- Implemented a demo blacklist and engine skip logic:
  - `core_v3/blacklist.json` created (contains `DE30`, `JP225`, `US30`).
  - `core_v3/engine.py` now loads `core_v3/blacklist.json` and will skip symbols that appear in the blacklist during scanning.
- Added SL safety floor in `core_v3/vault_v2.py` to prevent negative or unrealistically tiny SL values.
- Implemented Telegram alert rate-limiting and quiet mode in `core_v3/signal_commander.py`.
- Created `janitor.py` and `JANITOR_SETUP.bat` for automated maintenance.

**How to view UI**
- Open the HTML dashboard in your browser:

  file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/nexus/sovereign_nexus.html

- Or open `http://127.0.0.1:5050` (API must be running via `nexus_bridge.py`).

**Start / Stop (recommended)**
- Start core_v3 fleet (master, sentinel, nexus_bridge, engines):

```bash
python core_v3/commander_control.py start
```

- Stop fleet:

```bash
python core_v3/commander_control.py stop
```

- Restart (stop then start)

**Blacklisted tickers**
- `core_v3/blacklist.json` lists tickers to never trade on demo (modify as required). Current default entries were taken from MT5 logs/screenshots showing `Invalid volume` errors:
  - `DE30`, `JP225`, `US30`

**Telegram / Alerts**
- Telegram credentials are in `core_v3/secrets.json`. Alerts are now rate-limited and quiet by default (set `quiet_mode=False` in `core_v3/signal_commander.py` to re-enable frequent alerts).

**Safety & Known Issues**
- MT5 may reject small volumes (`Invalid volume (Code: 10014)`) — adjust lot sizing in `core_v3/vault_v2.py` or your broker's minimum lot settings.
- `core_real` remains incomplete — do not attempt to launch it until `core_real/engine.py` and `core_real/vault_v2.py` are populated and integrity checks pass.

**Maintenance**
- Run janitor immediately:

```bash
python janitor.py --run
```

- To schedule daily maintenance: run `JANITOR_SETUP.bat` as Administrator.

**Troubleshooting**
- If UI shows stale or zero values: verify `nexus_bridge.py` is running on port `5050`.
- If a bot fails to place an order: check `*_engine.log` for `Invalid volume` or symbol-specific errors; add offending tickers to `core_v3/blacklist.json`.
- To check DB integrity:

```bash
python -c "import sqlite3; print(sqlite3.connect('core_v3/iron_core.db').execute('PRAGMA integrity_check').fetchone())"
```

**Next recommended steps**
1. Review `core_v3/blacklist.json` and add any symbols your demo broker rejects.
2. Tune lot-sizing parameters in `core_v3/vault_v2.py` to match broker minimums.
3. If you want to deploy `core_real`, port the `core_v3` implementations into `core_real/` and re-run integrity tests.

---

**Critical Operational Update (May 06, 2026 - Hardening Phase)**

**1. Emergency Physical Kill-Switch:**
- Created [**`KILL_SWITCH.bat`**](file:///c:/Users/ADMIN/Desktop/IRON_COMMANDER_ELITE/KILL_SWITCH.bat) in the root directory.
- **Function:** Forcefully terminates all `python.exe` processes and updates `iron_core.db` (`GLOBAL_PAUSE = 1`) to lock the system state. Use this if the Web UI is unreachable.

**2. Tactical API Expansion (`nexus_bridge.py`):**
- `/api/sync` [POST]: Forces a re-fetch of MT5 health and clears internal cache.
- `/api/tactical/stop` [POST]: Triggers a database-level Global Pause.
- `/api/tactical/reinforce` [POST]: Scales unit `LOT_SIZE` (x1.5) and `DCA_LAYERS` (+2) in `DNA.json`. Supports `action='reset'`.
- `/api/reports/equity_curve` [GET]: Serves 100-point equity data from `trades` table for the Battle Report.

**3. UI & Report Synchronization:**
- `sovereign_nexus.html`: Hardened the `updateHUD` loop with defensive null-checks. Linked all Control Bar buttons to live APIs.
- `elite_report.html`: Fixed broken Chart.js binding and restored the `strike-log` tactical container. Served via `/report`.

**4. Coder's Self-Correction Protocol (To be archived by Docs):**
- **Endpoint Collision:** Always `grep` for route names before adding new ones to Flask.
- **Import Scoping:** Core libs (`datetime`, `os`) must be global to prevent `NameError` during async execution.
- **Foreground Testing:** New bridge scripts must be validated in the terminal (foreground) before running with `start` (background).

---
**Handover Status:** Technical details ready for Docs integration.

---

**🔥 COMMANDER's STRICT DIRECTIVE (MAY 06, 2026) 🔥**
*Attention Documentation Agent: The following MUST be permanently inscribed into the primary protocol (`AGENT_PROTOCOL.md` / `SHIPMENT_TRACKER.md`):*

1. **NO GUESSWORK:** All coders are required to be **EXTREMELY CAREFUL** when editing live files.
2. **VERIFY BEFORE DEPLOY:** Do not assume a simple UI or backend change will "just work". You must verify variable names, check for namespace/route collisions (e.g., Flask duplicate routes), and validate floating-point math (e.g., precise MT5 Lot/Volume steps).
3. **5-MINUTE RULE ENFORCED:** Any failure to double-check these details that results in a system crash or broken UI will be considered a severe breach of operational protocol. Measure twice, code once.
**Coder Agent:** Antigravity
