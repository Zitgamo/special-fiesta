# 🛡️ SOVEREIGN KNOWLEDGE BASE: MANIFESTO

This directory serves as the "Sovereign Memory" for the Iron Commander Elite fleet. It is organized by **Tactical Zones** to ensure rapid bug diagnosis and hardened resolution.

## 🗺️ Tactical Zones

### 1. [FRONTEND Zone](FRONTEND.md)
**Scope**: `nexus/sovereign_nexus.html`, `nexus/southern_command.html`, and CSS/JS rendering.
- **Critical Gotcha**: Chrome 3D rendering (Overflow bug).
- **Critical Gotcha**: Flexbox height collapse in fixed-height grids.
- **Protocol**: Currency detection (VN30F1M -> VNĐ).

### 2. [BACKEND Zone](BACKEND.md)
**Scope**: `core_v3/`, Python logic, MT5 bridge, and SQLite database.
- **Critical Gotcha**: SQLite WAL (Write-Ahead Logging) necessity for concurrency.
- **Protocol**: Silent Terminal (No vocal/media synthesis).
- **Protocol**: Signal Deduplication (1-hour cooldown).

### 3. [OPERATIONAL Zone](PROTOCOLS.md)
**Scope**: Deployment modes, Stress tests, and Git synchronization.
- **Critical Gotcha**: 12-hour stability threshold (43,200s).
- **Protocol**: "Fail-Closed" architectural integrity.

---
**Diagnosis Workflow**:
1. Identify the symptom (Visual? Logic? Data flow?).
2. Match to a Zone.
3. Consult the Zone-specific Hardening Document before attempting a fix.
