# 🚀 ZONE: OPERATIONAL PROTOCOLS (SBTP v1.0)

This document tracks deployment procedures, stress-test verification, and "Fail-Closed" safety rules.

## 🛡️ Sovereign Battle-Testing Protocol (SBTP)
For all future version deployments (v10.0+), the following tracking mechanisms are **MANDATORY**:

### 1. Telegram Milestone Telemetry
- **Auto-Broadcast**: The Ghost Comm bot must alert the commander at specific test percentages:
  - **25% (Tactical Foothold)**: Preliminary stability confirmed.
  - **50% (Strategic Parity)**: Half-way mark; perform DB WAL check.
  - **75% (Dominance Established)**: High-stress endurance confirmed.
  - **100% (Sovereign Victory)**: Final forensic audit ready.
- **On-Demand**: `/test_status` command must return Time Left, Current Uptime, and Peak Memory usage.

### 2. UI Visual Milestones
- **Progress Markers**: The `#uptime-progress` bar must include vertical segment markers at 25/50/75%.
- **Badge System**: A "Test Phase" badge in the header must change color based on progress (e.g., Bronze -> Silver -> Gold -> Platinum).

### 3. Forensic State Snapshots
- **Interval Checks**: Every 3 hours (for a 12H test), `janitor.py` must take a snapshot of the `iron_core.db` and current log sizes.
- **Zero-Crash Integrity**: Uptime must be tracked independently of the `nexus_bridge.py` server to ensure true backend persistence.

## 🚨 Identified Bug Zones

### 1. Stress Test Stability Audit
- **Goal**: 12 hours (43,200 seconds) of 100% uptime with ZERO crashes.
- **Verification**: Check `logs/sentinel_crash.log` and the `UPTIME` tracker in the Nexus header.
- **Rule**: Any UI change MUST be verified client-side without restarting the `nexus_bridge.py` server to preserve test continuity.

### 2. REAL vs DEMO Safety Lock
- **Protocol**: The "Master Arm" and "Deploy Mode" switches in the Nexus footer are the final gates.
- **Verification**: `REAL` mode must always prompt for user confirmation and show a red border on the mode toggle.

### 3. Fleet Synchronization (Git)
- **Protocol**: Use `git_sync.py` to ensure local changes are synchronized across all terminal instances.
- **Rule**: If `[!] UNCOMMITTED CHANGES` appears in the audit tab, verify disk state before scaling units.
