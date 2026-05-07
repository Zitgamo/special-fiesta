# 🛠️ SOVEREIGN CODER — STANDARD OPERATING PROCEDURE (SOP)
## [The Coder's Oath of Integrity]

Every AI Agent or Developer entering this project must follow these steps to ensure the fleet remains stable and the documentation remains canonical.

---

## 1. INITIALIZATION (The First Look)
Upon starting a new session or window:
1.  **Read the Index**: Open [**docs/00_INDEX.md**](../../docs/00_INDEX.md) immediately.
2.  **Scan the Horizon**: Check [**docs/HANDOVER/CURRENT_MISSION.md**](../../docs/HANDOVER/CURRENT_MISSION.md) to understand the active objective.

## 2. PRE-FLIGHT AUDIT (The Mine Check)
Before modifying any logic in `core_v3/` or `nexus/`:
1.  **Check the Error Log**: Search [**docs/ERRORS/ERROR_LOG.md**](../../docs/ERRORS/ERROR_LOG.md) for the specific component.
2.  **Verify Permissions**: Check [**docs/PROTOCOL/CODING_RULES.md**](../../docs/PROTOCOL/CODING_RULES.md) for the **LOCKED** file list.

## 3. EXECUTION & LOGGING (The Evolution)
1.  **Maintain the Librarian**: If you encounter a new bug and fix it, you MUST call:
    `python librarian.py --log "DESCRIPTION" "FIX_APPLIED" "AFFECTED_FILE"`
2.  **Keep the Index Fresh**: After adding new protocols or files, call:
    `python librarian.py --update`

## 4. SHIPMENT (The Handover)
Before ending your session:
1.  Update [**docs/HANDOVER/DONE_LOG.md**](../../docs/HANDOVER/DONE_LOG.md) with your achievements.
2.  Push your changes to the **PRIVATE** Sovereign Cloud (GitHub).
3.  Prepare a clean release if required: `python librarian.py --release`.

---
**Status:** [ENFORCED BY .CURSORRULES]
**Motto:** *"Documentation is the armor of the empire. Do not let it rust."*
