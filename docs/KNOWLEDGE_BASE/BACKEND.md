# ⚙️ ZONE: BACKEND HARDENING

This document tracks core logic, data flow, and bridge vulnerabilities for the `core_v3` architecture.

## 🚨 Identified Bug Zones

### 1. Database Concurrency Lock (SQLite)
- **Bug**: `database is locked` errors during high-frequency trading or multi-unit deployment.
- **Cause**: SQLite default journal mode doesn't handle multiple concurrent reads/writes well.
- **Solution**: Enforce **WAL (Write-Ahead Logging)** mode on the database connection.
- **Status**: [HARDENED] in `iron_core.db`.

### 2. Silent Terminal Protocol
- **Bug**: Unwanted vocal or media synthesis disrupting the silent trading environment.
- **Cause**: Legacy modules or 3rd party libraries attempting to play sounds/voice.
- **Solution**: Purge all `win32com.client` Dispatch calls for `SAPI.SpVoice` and media playback loops.

### 3. Signal Relay Spam
- **Bug**: Telegram receiving duplicate or excessive trade signals.
- **Cause**: Signal loops triggering multiple times per price tick.
- **Solution**: Implement a **1-hour cooldown** (deduplication) based on `symbol` and `signal_type`.
