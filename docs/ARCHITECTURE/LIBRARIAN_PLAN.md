# 🗺️ LIBRARIAN AGENT — FULL IMPLEMENTATION PLAN
## [The Sovereign Documentation Architecture]

This document preserves the 5-Day Roadmap for the Librarian Agent's deployment and maintenance.

---

## 🏗️ STEP 1: CANONICAL FOLDER STRUCTURE
All documentation must follow this hierarchy to ensure AI Agents can navigate the codebase instantly:

```text
docs/
├── 00_INDEX.md              ← THE MAP (librarian updates this only)
├── ERRORS/
│   └── ERROR_LOG.md         ← Every bug ever hit + fix applied
├── PROTOCOL/
│   ├── CODING_RULES.md      ← What not to touch, naming rules
│   ├── DEPLOY_PROTOCOL.md   ← How to launch, test, ship
│   └── RELEASE_PROTOCOL.md  ← Commercial release rules
├── ARCHITECTURE/
│   ├── SYSTEM_MAP.md        ← What each file does (one-liner)
│   ├── DNA_ENGINE.md        ← Logic for genetic mutation
│   └── LIBRARIAN_ORIGIN.md  ← Why this agent exists
└── HANDOVER/
    ├── CURRENT_MISSION.md   ← What we are doing right now
    └── DONE_LOG.md          ← History of completed milestones
```

## 🤖 STEP 2: THE LIBRARIAN AGENT (librarian.py)
The Python-based gatekeeper for the `docs/` folder.

- **QUERY**: Search all `.md` files for specific components or past errors.
- **LOG_ERROR**: Append structured fixes to `ERROR_LOG.md`.
- **UPDATE_INDEX**: Rebuild the Master Index based on current file states.
- **GUARD_CHECK**: Warn if an agent tries to edit a `LOCKED` file.
- **RELEASE**: Prepare a clean customer-ready bundle.

## 🧹 STEP 3: MIGRATION & POPULATION
- **Surgical Cleanup**: Delete legacy `.md` files (README.old, test_results.txt) and consolidate into the new structure.
- **System Mapping**: Every file in the root and `core_v3/` must have a corresponding entry in `SYSTEM_MAP.md`.
- **Bug Backfill**: Migrate historical bugs from `DEV_BUG_LOG` into `ERROR_LOG.md`.

## 🛡️ STEP 4: GITHUB SECURITY AUDIT
- **Secrets Check**: Ensure `secrets_real.json` is never tracked by Git.
- **History Scrub**: Use `git filter-branch` to erase historical leaks (2GB files, credentials).
- **Privacy Lock**: Maintain the repository as PRIVATE.

## 🛠️ STEP 5: CODER AGENT INSTRUCTIONS
Before writing any code, every AI agent must:
1. Read `docs/00_INDEX.md` first (30 seconds, saves hours).
2. Search `ERRORS/ERROR_LOG.md` for the component they are touching.
3. Check `PROTOCOL/CODING_RULES.md` for locked files.
4. After completing work: call `librarian.log_error()` if any bug was hit, and update `HANDOVER/CURRENT_MISSION.md`.

---
**Status:** [ENFORCED]
**Commander Directive:** *"Documentation is the armor of the empire. Do not let it rust."*
