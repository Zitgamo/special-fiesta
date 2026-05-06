# 🛠️ Utility Scripts

This project includes several utility scripts for maintenance, synchronization, and system health.

## 🧹 Sovereign Janitor (`janitor.py`)
The **Sovereign Janitor** is an automatic maintenance and cleanup agent designed to keep the project healthy.
- **Functions:**
  - Cleans up logs older than 7 days.
  - Removes temporary files (`.tmp`, `.pyc`, `__pycache__`, etc.).
  - Archives databases older than 30 days to `03_DATA/archive`.
  - Validates SQLite database integrity.
  - Checks JSON configuration files for syntax errors.
- **Usage:**
  ```powershell
  python janitor.py --run
  ```
- **Scheduling:** It is recommended to schedule this script daily at 2:00 AM using Windows Task Scheduler.

## 🔄 Git Sync (`git_sync.py`)
A utility script to ensure the codebase is synchronized across environments.
- **Usage:**
  ```powershell
  python git_sync.py
  ```

## 🚀 Mission Recovery (`MISSION_RECOVERY.bat`)
A failsafe batch script to restart the entire sovereign fleet if a catastrophic system failure occurs.
- **Usage:** Double-click the file or run via terminal:
  ```powershell
  ./MISSION_RECOVERY.bat
  ```

## 🧰 Diagnostic Tools (core_v3/)
The following scripts in `core_v3/` are used for rapid system checks:
- **`check_audusd.py` / `check_binance.py`:** Verifies connectivity to specific symbols or exchanges.
- **`system_integrity_check.py`:** Performs a deep audit of the engine's health before a trading session.
- **`force_scan.py`:** Manually triggers a market discovery scan.

---
**Note:** Always run utility scripts from the project root directory.
