# ⚖️ SOVEREIGN PURGATORY PROTOCOL (v1.0)
## [The Law of the Shadow Resurrection]

This protocol ensures that no tactical unit is ever "retired" permanently due to temporary market cycles. It establishes a "Shadow Purgatory" for quarantined units to prove their redemption.

### 1. MANDATORY PERSISTENCE
- **NO DELETION**: A unit marked `QUARANTINE: true` in `dna.json` MUST NOT be stopped.
- **SHADOW EXECUTION**: The `engine.py` MUST continue to run the "Oracle Scan" for quarantined units.
- **VIRTUAL STRIKES**: If a quarantined unit triggers a "Strike," it must be recorded in the `iron_core.db` as a `type = 'SHADOW_PURGATORY'` trade. No real capital is to be risked.

### 2. THE REDEMPTION AUDIT (CRITIC)
- **FORENSIC MONITORING**: The `AdversarialCritic` must audit Shadow Purgatory trades every 24 hours.
- **REBIRTH CRITERIA**: A unit is eligible for "Resurrection" if:
    1. It has completed at least 10 Shadow Strikes.
    2. Its Shadow Win Rate is > 55%.
    3. Its Shadow Expectancy is positive (> 0.2 ER).

### 3. THE RESURRECTION HANDOVER
- Once a unit is redeemed, the `DNAEngine` will:
    1. Set `QUARANTINE: false`.
    2. Reset its `VETERANCY_RANK` to 1 (Probation).
    3. Broadcast a "REBIRTH ALERT" to the Commander via Telegram.

### ⚠️ ANTI-REMOVAL MANDATE
This protocol is a **CORE SOVEREIGN PILLAR**. Any AI or Developer attempting to remove the Shadow Purgatory logic to "save CPU" or "simplify code" is in direct violation of the **Sovereign Philosophy**.

---
**Protocol Motto:** *"Even the shadows serve the Empire. Data is more valuable than idle CPU."*
