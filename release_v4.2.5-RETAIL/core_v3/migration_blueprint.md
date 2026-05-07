# Sovereign Migration Blueprint: Operation "Hardened Core"

This document outlines the final tactical maneuver to transition all trading operations into the `core_v3` architecture and archive the legacy root-level infrastructure.

## 🎯 Objectives
1.  **Consolidation**: Move all active logic to the `core_v3` hardened directory.
2.  **Redundancy**: Maintain legacy databases as read-only emergency fallbacks.
3.  **Persistence**: Ensure the `IronSentinel` manages the entire `core_v3` stack.

## 🛠️ Step 1: Database Synchronization (One-Time)
Run the backfill script to ensure all historical XP is accounted for in `core_v3/iron_core.db`.
```bash
python scratch/backfill_xp.py
```

## 🛠️ Step 2: Protocol Migration
The following root-level files are now **DEPRECATED**. Their functionality has been moved to `core_v3`:
- `commander.py` -> `core_v3/master.py`
- `mayday_sentinel.py` -> `core_v3/sentinel.py`
- `equity_snapshotter.py` -> `core_v3/equity_snapshotter.py`
- `tactical_map.py` -> To be updated to point to `iron_core.db`.

## 🛠️ Step 3: Sentinel Lockdown
Update `core_v3/sentinel.py` to ensure it only monitors `core_v3` processes.
- [x] Done in Sentinel v3.0.

## 🛠️ Step 4: Archive Legacy
Move all root-level `.py` and `.db` files (except `SovereignOS.jsx`) to a `legacy_archive/` folder.

## 🛡️ Step 5: Activation
Launch the entire fleet from the core:
```powershell
python core_v3/commander_control.py start all
```

---
**COMMANDER NOTE**: "We no longer fight in the open. The Core is our fortress."
