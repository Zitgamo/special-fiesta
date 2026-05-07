# 🚀 SOVEREIGN COMMERCIAL RELEASE PROTOCOL (v1.0)
## Objective: Transforming Dev-Core into a Customer-Facing Product

This protocol defines the "Surgical Separation" between **Development (Sovereign Elite)** and **Distribution (Sovereign Retail)**.

---

## 🛡️ 1. THE "ZERO-NOISE" AUDIT
Before any public release or shipment to a customer, the Librarian must verify the absence of:
- [ ] **Developer Artifacts**: `librarian.py`, `docs/`, `scratch/`, `git_sync.py`.
- [ ] **Internal Logs**: `*.log`, `debug/`, `logs/`.
- [ ] **Security Leaks**: `secrets_real.json`, `*.db`.
- [ ] **Engineering Batches**: `STRESS_WATCHDOG.bat`, `MISSION_RECOVERY.bat`, `JANITOR_SETUP.bat`.

## 📦 2. THE RETAIL BUNDLE (What the customer sees)
The final distribution folder MUST only contain:
1.  `core_v3/` (The engine logic)
2.  `nexus/` (The UI dashboard)
3.  `LAUNCH_SOVEREIGN.bat` (Renamed from `REAL_LAUNCH`)
4.  `janitor.py` (Hidden maintenance)
5.  `README_CUSTOMER.md` (Installation and user guide)
6.  `secrets.json` (TEMPLATE ONLY - empty credentials)

## 🏛️ 3. LIBRARIAN RELEASE GATE
The Librarian Agent (`librarian.py`) will now act as the **Release Guardian**.
- **Action**: `python librarian.py --release`
- **Function**:
    1. Scans the root for any file marked as `INTERNAL_ONLY` in `SYSTEM_MAP.md`.
    2. Automatically creates a `release_vX.Y.Z/` directory.
    3. Copies only the "Retail Bundle" components.
    4. Scrubs the `dna.json` of any experimental or high-risk test parameters.

## 🏁 4. SHIPMENT VERIFICATION
A release is considered **"Sovereign Certified"** only if:
1.  It is tagged in a **PRIVATE** secondary repository or a clean branch.
2.  No commit history from the "Dev" branch is carried over (Squash and Merge).
3.  The UI displays the correct Version Hash and "Retail Mode" badge.

---
**Protocol Motto:** *"Professionalism is the absence of the unnecessary."*
