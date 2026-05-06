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

If you want, I can:
- Apply a dynamic broker-minimum lot check to avoid `Invalid volume` errors automatically.
- Roll out the blacklist enforcement to `core_real` when ready.
- Push this handover into a `handover/` folder and create a quick checklist ticket.
